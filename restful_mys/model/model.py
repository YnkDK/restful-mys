from ..common.data.postgresql_adapter import PostgreSQL
from ..common.data.csv_adapter import CSV


class Model(PostgreSQL, CSV):
    def __init__(self):
        """
        Initializes super classes
        """
        PostgreSQL.__init__(self)
        CSV.__init__(self)

    def __del__(self):
        """
        Invokes deletion in super classes
        """
        PostgreSQL.__del__(self)
        CSV.__del__(self)