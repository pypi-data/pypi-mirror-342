from .metadata import Metadata
from .table import Table
from .executer import Executer
from .sub_table import SubTable

if __name__ == "__main__":

    schema = "schema1"
    table_name = "table1"
    metadata = Metadata(schema)
    print("Metadata:", metadata.get_table(table_name))
    table = Table(f"{schema}/{table_name}", metadata.get_table(table_name))
    
    query = {
        'columns': ['table1.*'],
        'tables': ['table1'],
        'conditions': [
            {'left_operand': 'age', 'operator': '<', 'right_operand': '30'}
        ]
    }
    executer = Executer()
    sub_table = executer.execute_query(query, metadata, schema)
    print("Table\n", table)
    print(sub_table)