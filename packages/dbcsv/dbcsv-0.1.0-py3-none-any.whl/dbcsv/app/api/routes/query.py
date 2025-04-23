from fastapi import APIRouter , Depends, HTTPException

from ..schemas.auth import User
from ..schemas.sql_request import SQLRequest
from ...core.parser.sql_parser import SQLParser
from ...core.storage_layer.executer import Executer
from ...core.storage_layer.metadata import Metadata
from ...dependencies import current_user_dependency
from typing import Annotated
from ...core.database_engine import DatabaseEngine, get_engine
from fastapi import HTTPException, status

router = APIRouter(
    prefix='/query',
    tags=['Query']
)

executer = Executer()

@router.post('/sql')
def query_by_sql(sql_request: SQLRequest, current_user: Annotated[User, current_user_dependency], database_engine: Annotated[DatabaseEngine, Depends(get_engine)]):
    try:
        table = database_engine.execute(sql_request.sql_statement, sql_request.schema)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return table.to_json()