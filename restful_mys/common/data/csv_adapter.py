import os
import csv

from flask.ext.restful import abort


class CSV(object):
    def __init__(self):
        self._csv = dict()

    def __del__(self):
        del self._csv

    def csv_add(self, alias, path):
        """
        Adds a CSV file to file base.

        :param alias: CSV alias in which the path can be found
        :param path: The path to the CSV file
        :return: True if added (path points to a file), False otherwise
        :rtype: bool
        """
        if os.path.isfile(path):
            self._csv[alias] = path
            return True
        return False

    def csv_remove(self, alias):
        """
        Removes a CSV file from file base.

        :param alias: CSV alias to be removed
        :return: True if alias was known, False otherwise
        :rtype: bool
        """
        if alias in self._csv:
            del self._csv[alias]
            return True
        return False

    def csv_read(self, alias, skip_line=1, **fmtparams):
        """
        Reads the CSV file known under the alias.

        :param alias: CSV alias to be read
        :param skip_line: Number of initial lines to be skipped. Defaults to the first line if not provided
        :param fmtparams: Other parameters necessary for the csv.reader
        :return: A generator
        """
        if alias not in self._csv:
            abort(
                500,
                message='Internal Server Error',
                method='data.csv.csv_read',
                error_message='Alias not found: {:s}'.format(str(alias))
            )

        with open(self._csv[alias], 'rb') as csv_file:
            csv_reader = csv.reader(csv_file, **fmtparams)
            for i in xrange(skip_line):
                # Skip some lines, headers etc.
                csv_reader.next()

            for row in csv_reader:
                # Simply yield each row
                yield row

    @staticmethod
    def csv_typed_row(row, indices, types):
        """
        Extracts and converts the elements on the given indices from the given row.
        :param row: An indexable data type.
        :param indices: Indices to be extracted.
        :param types: A tuple of callable entries, which transforms an object to a certain type
        :return: A tuple of the same length and order as the parameter indices, but with typed values
        :rtype: tuple
        """
        if len(indices) != len(types):
            abort(
                500,
                message='Internal Server Error',
                method='data.csv.csv_typed_row',
                error_message='Each output entry must have a type, i.e. "indices" and "types" must have same length'
            )

        res = []
        for i, t in zip(indices, types):
            # Strip the string in both ends
            cur = row[i].strip()
            if cur == '':
                # '' is None (null in database)
                res.append(None)
            else:
                try:
                    typed = t(cur)
                except TypeError:
                    abort(
                        500,
                        message='Internal Server Error',
                        method='data.csv.csv_typed_row',
                        error_message=TypeError.message
                    )
                else:
                    res.append(typed)
        return tuple(res)