from .table import Table

class SubTable(Table):
    def __init__(self, columns: list[str], column_types: list[str], data: list[list[str]]):
        self.table_name = "SubTable"
        self._columns = columns
        self._column_types = column_types
        self._data = data
    

    def __str__(self):
        return super().__str__()       