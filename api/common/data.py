import psycopg2
import csv
import os.path

class Data(object):
	def __init__(self):
		self._pgsql = None
		self.csv = dict()
		# TODO: Support this
		self.shelves = dict()
	
	def __enter__(self):
		""" Object scope was started. Make it
			available :-)
		"""
		return self		
	
	def __exit__(self, type, value, traceback):
		""" Data object was deleted. Say goodbye
		    to the database. Bye bye!
		"""
		# Explicit delete CSV dictionary
		del self.csv
		
		if self._pgsql is not None:
			# If a postgresql connection
			# was established, close it
			self._pgsql.close()	

		for key in self.shelves.keys():
			# Close all open shelves
			self.shelves[key].close()
			
	def pgsqlConnect(self, database, user, password, host = 'localhost', port = '5432', connection_factory=None, cursor_factory=None, async=False, autocommit=True):
		""" Sets the class variable pgsql as the connection
		    to a postgresql database.
		"""
		self._pgsql = psycopg2.connect(
			database = database,
			user = user,
			password = password,
			host = host,
			port = str(port)
		)
		self._pgsql.autocommit = autocommit
	
	def pgCursor(self):
		""" Returns a cursor object for
		    the postgresql connection
		    or None if connection not
		    open.
		"""
		return self._pgsql.cursor() if self._pgsql is not None else None

	def select(self, cols, table, where = None, params = None):
		""" NOTICE: THE PARAMETERS "cols", "table"
			        AND "where" IS _NOT_ ESCAPED.
			        THEY MUST NEVER BE END-USER INPUT.
			        THE PARAMETER "param" _IS_ ESCAPED
			
			Selects the "cols" (or all if cols = None)
			from "table". If "where" is not None, then
			it must be a string of form
			"col1 = %s AND col2 = %s", and params must
			be an iterable of the length corresponding
			to the number of "%s" in "where".
			
			Yields each row returned (None if empty)
			from a select query on the postgresql
			connection.
		"""
		stm = "SELECT "
		if cols is None:
			stm += "* "
		else:
			stm += "{:s} ".format(cols)
		stm += "FROM {:s} ".format(table)
		
		with self._pgsql.cursor() as cur:
			if where is not None:
				stm += "WHERE {:s};"
				stm = cur.mogrify(stm, args)
			cur.execute(stm)
			for row in cur.fetchall():
				yield row
	
	def insert(self, cols, table, values):
		""" NOTICE: THE PARAMETERS "cols" AND "table"
			        IS _NOT_ ESCAPED. THEY MUST NEVER
			        BE END-USER INPUT. THE PARAMETER
			        "values" _IS_ ESCAPED
			Inserts "values" into "table" in the corresponding
			"cols"
			
			Invokes an insert on the postgresql connection.
			
			Returns: Number of elements inserted
		"""
		values = tuple(values)
		if len(values) == 0:
			# If we should not insert anythin, just return 0
			return 0
			
		stm = "INSERT INTO {:s} ({:s}) VALUES ".format(table, cols)
		with self._pgsql.cursor() as cur:
			s = '(' + ','.join(['%s']*len(values[0])) + ')'
			for i in xrange(0, len(values), self.chunkSize):
				# Some stm might become to long to transmit,
				# thus sending in smaller chunks might help
				args_str = ','.join(cur.mogrify(s, x) for x in values[i:i+chunkSize])
				cur.execute(stm + args_str)		
		
		return len(values)
	
	def update(self, table, where, what, values):
		""" NOTICE: THE PARAMETERS "table", "where",
			        AND "what" IS _NOT_ ESCAPED. THEY
			        MUST NEVER BE END-USER INPUT.
			        THE PARAMETER "values" _IS_ ESCAPED
			Finds the columns "where" the "values" matchs
			in "table" and sets "what" according to "values".
			
			Invokes an update on the postgresql connection.
			
			Returns: Number of elements updated
		"""		
		if len(values) == 0:
			return 0
		stm = "UPDATE {:s} SET {:s} WHERE {:s};".format(table, what, where)
		with self._pgsql.cursor() as cur:
			cur.executemany(stm, values)
		return len(values)
		
	def addCSV(self, alias, path):
		""" Adds a "path" to a file under
		    the "alias" given, only if the
		    path is a file.
		    
		    Returns: True if added, False otherwise
		"""
		if os.path.isfile(path):
			self.csv[alias] = path
			return True
		return False
	
	def removeCSV(self, alias):
		""" Removes an alias from CSV paths
		"""
		if alias in self.csv:
			del self.csv[alias]
			return True
		return False
		
	def read(self, alias, skipLine = 1, **fmtparams):
		""" Reads a CSV file defined by an "alias",
		    but skipping "skipLine" lines first.
		"""
		if alias not in self.csv:
			return
			
		with open(self.csv[alias], 'rb') as csvfile:
			csvReader = csv.reader(csvfile, **fmtparams)
			for i in xrange(skipLine):
				# Skip some lines, headers etc.
				csvReader.next()
			
			for row in csvReader:
				# Simply yield each row
				yield row		
		
	def typeRow(self, row, indices, types):
		""" Extract and converts the element
		    on the given indices from the given
		    row. 
		    
		    Raises IndexError if indices and types
		    are not of the same length
		    Raises TypeError if an entry in types
		    are not callable.
		    
		    Returns: A tuple of the same length 
		    and order as indices, but with typed
		    values.
		"""
		if len(indices) != len(types):
			raise IndexError("Each output entry must have a type")
		res = []
		for i,t in zip(indices, types):
			# Strip the string in both ends
			cur = row[i].strip()			
			if cur == '':
				# '' is None (null in database)
				res.append(None)
			else:
				res.append(t(cur))
		return tuple(res)
