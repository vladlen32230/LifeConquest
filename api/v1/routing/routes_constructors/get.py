from models.other import Route
from models.sqlalchemy import SaBase, SaUser
from models.pydantic.returning import PdBase
from typing import Annotated, Callable
from fastapi import Depends
from dependencies.queries.get import GetObjectByIdPathV1

def construct_get_by_id_route_v1(
    sa_entity: type[SaBase], 
    pd_entity: type[PdBase], 
    permissions_checker: Callable[[SaUser, SaBase], bool] | None = None
) -> dict:
    get_object_request = GetObjectByIdPathV1(sa_entity, permissions_checker, pd_entity)
    status_code = 200
    entity_name = sa_entity.get_table_name()

    async def _endpoint(
        pd_instance: Annotated[SaBase, Depends(get_object_request.exc)]
    ):
        return pd_instance

    _endpoint.__name__ = f'get_{entity_name}_by_id_v1'

    return Route(
        path=f'/{entity_name}' + '/{id}',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=pd_entity,
        responses=get_object_request.responses,
        methods=['GET'],
        description=f'Get {entity_name} by id'
    ).__dict__