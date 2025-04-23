import csv
import os
import json
from pathlib import Path

DB_DIR = str(Path(__file__).parent.parent.parent.parent / "data")
class Table:

    # path: schema/table_name
    def __init__(self, path: str, metadata: dict[str, str] = None):
        self.schema = path.split("/")[-2]
        self.table_name = path.split("/")[-1]
        self._columns = list(metadata.keys()) if metadata else []
        self._column_types = list(metadata.values()) if metadata else []
        self._data = []
        self.load_from_csv(path)

    
    def load_from_csv(self, path: str):
        schema = path.split("/")[-2]
        table = path.split("/")[-1]
        schema, table = schema.lower(), table.lower()
        data_file_name = table + ".csv"
        data_path = os.path.join(DB_DIR, schema, data_file_name)
        try:
            with open(data_path, "r") as f:
                reader = csv.reader(f)
                # Get the header and compare it with the columns metadata
                header = next(reader)
                if len(header) != len(self._columns):
                    raise ValueError(f"Header length does not match column length in {schema}/{table}.")
                if any(col.lower() != header[i].lower() for i, col in enumerate(self._columns)):
                    raise ValueError(f"Header names do not match column names in {schema}/{table}.")
                # Read the data
                self._data = [row for row in reader]

        except FileNotFoundError:
            raise FileNotFoundError(f"{schema}/{table} not found.")
        except Exception as e:
            raise Exception(f"Error get {schema}/{table}: {e}")
        

    def save_to_csv(self, path: str):
        schema, table = path.split("/")
        schema, table = schema.lower(), table.lower()
        data_file_name = table + ".csv"
        metadata_path = os.path.join(DB_DIR, "metadata.txt")
        data_path = os.path.join(DB_DIR, schema, data_file_name)
        try:
            with open(data_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self._columns)
                writer.writerows(self._data)
        except Exception as e:
            raise Exception(f"Error writing to {schema}/{table}: {e}")
        try:
            with open(metadata_path, "a") as f:
                f.write(f"[{table}]\n")
                for col, col_type in zip(self._columns, self._column_types):
                    f.write(f"{col}={col_type}\n")
        except Exception as e:
            raise Exception(f"Error writing to {schema}/{table}: {e}")

        

    def __str__(self):
        result = f"Table: {self.table_name}\n"
        collumns = [f"\n\t{col} ({typ})" for col, typ in zip(self._columns, self._column_types)]
        result += f"Columns: {''.join(collumns)}\n"
        
        col_widths = [max(len(str(cell)) for cell in [col] + [row[i] for row in self._data]) for i, col in enumerate(self._columns)]

        header = [h.ljust(width) for h, width in zip(self._columns, col_widths)]
        result += " | ".join(header) + "\n"
        result += "-" * (sum(col_widths) + 3 * (len(header) - 1)) + "\n"

        for row in self._data:
            row_str = [str(cell).ljust(width) for cell, width in zip(row, col_widths)]
            result += " | ".join(row_str) + "\n"

        return result
    
    def to_json(self):
        result = {
            "table_name": self.table_name,
            "columns": self._columns,
            "column_types": self._column_types,
            "data": self._data
        }
        return json.dumps(result, indent=4)

    @property
    def data(self):
        return self._data

    @property
    def columns(self):
        return self._columns

    @property
    def column_types(self):
        return self._column_types

