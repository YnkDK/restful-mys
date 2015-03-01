# coding=utf-8
import psycopg2

from flask.ext.restful import abort


try:
    from ..config import PG_DB
except ImportError:
    PG_DB = None


class PostgreSQL(object):
    # With large inserts, it might be necessary to insert in chunks
    PG_CHUNCK_SIZE = 200000

    def __init__(self):
        """
        Sets up PostgreSQL connections defined in the config variable PG_DB.
        """
        self._pg_db = dict()

        if PG_DB is not None:
            if 'default' in PG_DB and PG_DB['default']['auto_connect']:
                self.PG_DEFAULT_DB = 'default'
            elif len(PG_DB.keys()) == 1 and PG_DB[PG_DB.keys()[0]]['auto_connect']:
                # If there is exactly one database defined
                # use this as default. In all other cases
                # it would be an arbitrary database, which
                # is pretty much useless
                self.PG_DEFAULT_DB = PG_DB.keys()[0]
            else:
                self.PG_DEFAULT_DB = None
            for alias, settings in PG_DB.iteritems():
                try:
                    if settings['auto_connect']:
                        self.pg_connect(
                            alias,
                            settings['database'],
                            settings['user'],
                            settings['password'],
                            settings['host'],
                            settings['port'],
                            settings['connection_factory'],
                            settings['cursor_factory'],
                            settings['async'],
                            settings['autocommit']
                        )
                except KeyError:
                    abort(
                        500,
                        message='Internal Server Error',
                        method='data.postgresql.__init__',
                        error_message=KeyError.message
                    )
        super(PostgreSQL, self).__init__()

    def __del__(self):
        """
        Close all connections upon deletion.
        """
        for name, connection in self._pg_db.iteritems():
            connection.close()

    def pg_connect(self, alias, database, user, password, host='localhost', port='5432', connection_factory=None,
                   cursor_factory=None, async=False, autocommit=False):
        """
        Returns an open connection to a PostgreSQL database, or aborts on error

        :param alias: Alias to identify the connection later
        :param database: The database alias
        :param user: User alias used to authenticate
        :param password: Password used to authenticate
        :param host: Database host address (defaults to localhost if not provided)
        :param port: Connection port number (defaults to 5432 if not provided)
        :param connection_factory: A different class or connections factory can be specified.
        :param cursor_factory: The connection’s cursor_factory is set to it
        :param async: Using async=True an asynchronous connection will be created
        :param autocommit: True: no transaction is handled by the driver False: new transaction at first command exec
        """
        try:
            pgsql = psycopg2.connect(
                database=database,
                user=user,
                password=password,
                host=host,
                port=str(port),
                connection_factory=connection_factory,
                cursor_factory=cursor_factory,
                async=async
            )
        except psycopg2.OperationalError as e:
            abort(500, message='Internal Server Error', method='data.postgresql.pg_connect', error_message=e.message)
        else:
            # Successfully connected: Honor autocommit setting
            pgsql.autocommit = autocommit
            self._pg_db[alias] = pgsql

    def pg_connection(self, alias=None):
        """
        Returns the connection associated with the given alias. If alias not found, the application aborts
        with status code 500

        :param alias: Connection alias (default to PG_DEFAULT_DB if not provided)
        :return: A PostgreSQL connection
        """
        try:
            connection = self._pg_db[self.PG_DEFAULT_DB if alias is None else alias]
        except KeyError:
            abort(
                500,
                message='Internal Server Error',
                method='data.postgresql.connection',
                error_message='Not connect to the database: {:s}'.format(str(alias))
            )
        else:
            return connection

    def pg_cursor(self, alias=None):
        """
        Returns a cursor object for the PostgreSQL connection
        or aborts with status code 500.

        :param alias: Connection alias (default to PG_DEFAULT_DB if not provided)
        :return: A cursor object for the PostgreSQL connection
        """
        return self.pg_connection(self.PG_DEFAULT_DB if alias is None else alias).cursor()

    def pg_select(self, cols, table, where=None, params=None, alias=None):
        """
        DISCLAIMER: THE PARAMETERS "cols", "table" AND "where" IS _NOT_ ESCAPED.
                    THEY MUST NEVER BE END-USER INPUT. THE ONLY PARAMETER THAT
                    CAN BE END-USER INPUT IS "param" WHICH IS ESCAPED

        Selects the "cols" (or all if cols = None) from "table". If "where" is not
        None, then   it must be a string of form "col1 = %s AND col2 = %s", and
        params must be an iterable of the length corresponding to the number of
        "%s" in "where".

        :param cols: Columns to be selected.
        :param table: Table to select from.
        :param where: Selection criteria (defaults to None if not provided)
        :param params: Selection parameters (defaults to None if not provided)
        :param alias: Connection alias (default to PG_DEFAULT_DB if not provided)
        :return: A generator for all results
        :rtype: generator
        """
        stm = "SELECT "
        if cols is None:
            stm += "* "
        else:
            stm += "{:s} ".format(cols)
        stm += "FROM {:s} ".format(table)
        alias = self.PG_DEFAULT_DB if alias is None else alias
        cur = self.pg_connection(alias).cursor()
        if where is not None:
            stm += "WHERE {:s};".format(where)
            stm = cur.mogrify(stm, params)

        cur.execute(stm)
        for row in cur.fetchall():
            yield row

    def pg_insert(self, cols, table, values, alias=None):
        """
        DISCLAIMER: THE PARAMETERS "cols" AND "table" IS _NOT_ ESCAPED. THEY MUST
                    NEVER BE END-USER INPUT. THE ONLY PARAMETER THAT CAN BE END-
                    USER INPUT IS "values" WHICH IS ESCAPED

        Invokes an insert on the given PostgreSQL connection.

        :param cols: Columns to be inserted.
        :param table: Table to insert to.
        :param values: Values of inserted columns
        :param alias: Connection alias (default to PG_DEFAULT_DB if not provided)
        :return: Number of rows affected
        :rtype: int
        """
        values = tuple(values)
        if len(values) == 0:
            # Nothing to insert
            return 0
        row_count = None
        with self.pg_cursor(self.PG_DEFAULT_DB if alias is None else alias) as cur:
            stm = 'INSERT INTO {:s} ({:s}) VALUES '.format(table, cols)
            # Construct a string in format (%s,%s,%s)
            s = '(' + ','.join(['%s'] * len(values[0])) + ')'
            for i in xrange(0, len(values), self.PG_CHUNCK_SIZE):
                # Some stm might become to long to transmit,
                # thus sending in smaller chunks might help
                args_str = ','.join(cur.mogrify(s, x) for x in values[i:i + self.PG_CHUNCK_SIZE])
                cur.execute(stm + args_str)
                row_count = cur.rowcount
        # Return 0 if row count is None or -1, otherwise the row count
        return 0 if row_count in [None, -1] else row_count

    def pg_update(self, table, where, what, values, alias=None):
        """
        DISCLAIMER: THE PARAMETERS "table", "where", AND "what" IS _NOT_ ESCAPED.
                    THEY MUST NEVER BE END-USER INPUT. THE ONLY PARAMETER THAT
                    CAN BE END-USER INPUT IS "values" WHICH IS ESCAPED

        Invokes one or many update(s) on the PostgreSQL connection.

        :param table: Table to be updated.
        :param where: Selection criteria.
        :param what: Columns to be updated.
        :param values: Selection parameters.
        :param alias: Connection alias (default to PG_DEFAULT_DB if not provided)
        :return: Number of affected rows
        :rtype: int
        """
        if len(values) == 0:
            return 0
        stm = "UPDATE {:s} SET {:s} WHERE {:s};".format(table, what, where)
        with self.pg_cursor(self.PG_DEFAULT_DB if alias is None else alias) as cur:
            cur.executemany(stm, values)
            row_count = cur.rowcount
        # Return 0 if row count is None or -1, otherwise the row count
        return 0 if row_count in [None, -1] else row_count