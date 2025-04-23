from pathlib import Path
import os
from .table import Table
from .sub_table import SubTable
from .table import Table
from .metadata import Metadata
from .datatypes import *
from .datatypes import convert_datatype


OPERATORS = {
    "=": lambda x, y: x == y,
    "==": lambda x, y: x == y,
    "!=": lambda x, y: x != y,
    "<>": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
}

class Executer:
    def __init__(self):
        pass

    def _load_table(self, table_name: str, schema: str, metadata) -> Table:
        path = f"{schema}/{table_name}"
        table = Table(path=path, metadata=metadata)
        return table


    def _check_condition(self, condition, row, columns, column_types):
    
        if not condition:
            return True
        
        columns = [col.upper() for col in columns]
        operator = condition["operator"]
        left_operand = condition["left_operand"]
        right_operand = condition["right_operand"]
        column_map = {col: i for i, col in enumerate(columns)}

        left_value = left_operand
        right_value = right_operand
    
        upper_left_operand = str(left_operand).upper()
        upper_right_operand = str(right_operand).upper()
        left_operand_type = ""
        right_operand_type = ""
        if upper_left_operand in columns:
            left_value = row[column_map[upper_left_operand]]
            left_operand_type = column_types[column_map[upper_left_operand]]
        if upper_right_operand in columns:
            right_value = row[column_map[upper_right_operand]]
            right_operand_type = column_types[column_map[upper_right_operand]]
        
        left_operand_type = right_operand_type if left_operand_type == "" else left_operand_type
        right_operand_type = left_operand_type if right_operand_type == "" else right_operand_type
        if upper_left_operand not in columns:
            left_value = convert_datatype(left_value, left_operand_type)
        if upper_right_operand not in columns:
            right_value = convert_datatype(right_value, right_operand_type)

        return OPERATORS[operator](left_value, right_value)
    
    def _evaluate_where_clause(self, table, conditions):
        if not conditions:
            return table

        filtered_data = []
        for row in table.data:
            if all(self._check_condition(cond, row, table.columns, table.column_types) for cond in conditions):
                filtered_data.append(row)

        filtered_table = SubTable(table.columns, table.column_types, filtered_data)
        return filtered_table
    
    def _select_columns(self, table: Table, columns: list):
            columns = [col.split(".")[-1] for col in columns]
            if "*" in columns:
                return table
            
            selected_data = []
            for row in table.data:
                selected_row = [row[table.columns.index(col)] for col in columns]
                selected_data.append(selected_row)
            
            new_table = SubTable(
                columns=columns,
                column_types=[table.column_types[table.columns.index(col)] for col in columns],
                data=selected_data
            )
            return new_table
    
    def execute_query(self, query: str, metadata: Metadata, schema: str) -> SubTable:
        selected_table = query.get("tables")[0]
        table = self._load_table(selected_table, schema, metadata = metadata.get_table(selected_table))
        conditions = query.get("conditions", [])
        selected_columns = query.get("columns", [])

        filtered_table = self._evaluate_where_clause(table, conditions)
        selected_table = self._select_columns(filtered_table, selected_columns)
        return selected_table
