from data.postgresql_adapter import PostgreSQL
from data.csv_adapter import CSV


class Model(PostgreSQL, CSV):
    def __init__(self):
        """
        Initializes super classes
        """
        super(Model, self).__init__()

    def __del__(self):
        """
        Invokes deletion in super classes
        """
        super(Model, self).__del__()