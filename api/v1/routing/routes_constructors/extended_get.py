from dependencies.queries.extended_get import ExtendedGetObjectsV1
from models.other import Route
from models.pydantic.extended import PdExtBase
from models.pydantic.returning import PdBase
from models.sqlalchemy import SaUser, SaBase
from typing import Callable, Annotated
from fastapi import Depends
from sqlalchemy import ColumnElement

def construct_extended_get_v1(
    sa_entity: type[SaBase],
    pd_get_extended: type[PdExtBase], 
    pd_entity: type[PdBase], 
    where_permissions_maker: Callable[[SaUser], ColumnElement[bool]] | None = None,
) -> dict:
    extended_get_request = ExtendedGetObjectsV1(sa_entity, pd_get_extended, pd_entity, where_permissions_maker)
    status_code = 200
    entity_name = sa_entity.get_table_name()

    async def _endpoint(
        pd_instances: Annotated[list[PdBase], Depends(extended_get_request.exc)]
    ):
        return pd_instances

    _endpoint.__name__ = f'extended_get_{entity_name}_v1'

    return Route(
        path=f'/extended/{entity_name}',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=list[pd_entity],
        responses=extended_get_request.responses,
        methods=['GET'],
        description=f'Get {entity_name} by filters'
    ).__dict__