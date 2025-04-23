import re
from typing import Any, Dict, Literal, Union, List
from fastapi import HTTPException

class SQLParser:
    BASIC_QUERY_PATTTERN = r"SELECT (.+?) FROM (.+?)(?: WHERE (.*))?$"
    CONDITION_PATTERN = r"(\w+)\s*(>=|<=|<>|<|>|=|)\s*(.+)"

    def __init__(self):
        self.columns: Union[List[str], Literal['*']] = []
        self.tables: List[str] = []
        self.conditions: List[Dict] = []

    @staticmethod
    def parse_where_clause(where_clause: str) -> List[Dict]:
        conditions = []
        for condition in re.split(r'\s+AND\s+', where_clause, flags=re.IGNORECASE):
            cond_match = re.match(SQLParser.CONDITION_PATTERN, condition.strip())
            if not cond_match:
                raise SyntaxError('Your WHERE clause is not valid')
            field, op, val = cond_match.groups()
            conditions.append({"left_operand": field, "operator": op, "right_operand": val})
        return conditions
    
    @staticmethod
    def parse_from_clause(from_clause: str) -> List[str]:
        from_clause = from_clause.strip()
        tables = [table.strip() for table in from_clause.split(',')]
        for table in tables:
            if not re.fullmatch(r'\w+', table):
                raise SyntaxError(f"near 'FROM clause': syntax error")
        return tables
            

    @staticmethod
    def parse_select_clause(select_clause: str, tables: List[str]) -> Union[List[str], Literal['*']]:
        select_clause = select_clause.strip()
        if select_clause == '*':
            return '*'
        
        columns = [col.strip() for col in select_clause.split(',')]
        for col in columns:
            if re.fullmatch(r"\w+", col):
                continue  
            elif re.fullmatch(r"\w+\.\*", col): 
                table_name = col.split('.')[0]
                if table_name not in tables:
                    raise SyntaxError(f"near SELECT clause: table '{table_name}' not found in FROM clause")
            elif re.fullmatch(r"\w+\.\w+", col):  
                table_name = col.split('.')[0]
                if table_name not in tables:
                    raise SyntaxError(f"near SELECT clause: table '{table_name}' not found in FROM clause")
            else:
                raise SyntaxError(f"near SELECT clause: invalid column format '{col}'")
        return columns

    @classmethod
    def from_sql(cls, query: str) -> 'SQLParser':
        parser = cls()
        query = ' '.join(query.strip().split())
        match_query = re.match(cls.BASIC_QUERY_PATTTERN, query, re.IGNORECASE)
        if not match_query:
            raise SyntaxError('SQL Format Error: invalid or unsupported sql statement format')
        
        select_clause = match_query.group(1).strip()
        from_clause = match_query.group(2).strip()
        where_clause = match_query.group(3).strip() if match_query.group(3) else None

        parser.tables = cls.parse_from_clause(from_clause)
        parser.columns = cls.parse_select_clause(select_clause, parser.tables)
        parser.conditions = cls.parse_where_clause(where_clause) if where_clause else []
        return parser
    
    def to_dict(self) -> Dict:
        return {
            'columns': self.columns,
            'tables' : self.tables,
            'conditions': self.conditions
        }





    
    
    
