import sys
from pathlib import Path
from fastapi import HTTPException

from ..core.storage_layer.metadata import Metadata
from ..core.storage_layer.sub_table import SubTable
from ..core.parser.sql_parser import SQLParser
from ..core.storage_layer.executer import Executer
import os


class DatabaseEngine():
    def __init__(self):
        self.__schemas : list[str] = self.__loadSchemas()
        self.__metadatas : dict[str, Metadata]= self.__loadMetadatas()  # Initialize the dict
        self.__executer = Executer()
    
    def __loadMetadatas(self) -> dict[str, Metadata]:
        self.__metadatas = {schema: Metadata(schema) for schema in self.__schemas}
        return self.__metadatas
    
    def __loadSchemas(self) -> list[str]:
        path = Path(__file__).parent.parent.parent / 'data' 
        schemas = [schema_name for schema_name in os.listdir(path) 
                  if os.path.isdir(Path(path) / schema_name)]
        return schemas

    def execute(self, sql_statement: str, schema: str) -> SubTable:
        if schema not in self.__schemas:
            raise HTTPException(status_code=404, detail=f"Schema {schema} not found!")
        parser = SQLParser.from_sql(sql_statement)
        metadata = self.__metadatas[schema]
        query = parser.to_dict()
        return self.__executer.execute_query(query, metadata, schema)
    
db_engine = DatabaseEngine()

def get_engine() -> DatabaseEngine:
    return db_engine