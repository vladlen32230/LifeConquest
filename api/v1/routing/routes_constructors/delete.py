from models.other import Route
from models.sqlalchemy import SaBase, SaUser
from typing import Callable, Annotated
from fastapi import Depends
from dependencies.db import get_session
from sqlalchemy.orm import Session
from queries.delete import delete_object
from dependencies.queries.get import GetObjectByIdPathV1

def construct_delete_by_id_route_v1(
    sa_entity: type[SaBase], 
    permissions_checker: Callable[[SaUser, SaBase], bool]
) -> dict:
    get_object_request = GetObjectByIdPathV1(sa_entity, permissions_checker)
    status_code = 204
    entity_name = sa_entity.get_table_name()

    async def _endpoint(
        sa_instance: Annotated[SaBase, Depends(get_object_request.exc)],
        session: Annotated[Session, Depends(get_session)]
    ):
        delete_object(sa_instance, session)
        return None
    
    _endpoint.__name__ = f'delete_{entity_name}_by_id_v1'

    return Route(
        path=f'/{entity_name}/' + '{id}',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=None,
        responses=get_object_request.responses,
        methods=['DELETE'],
        description=f'Delete {entity_name} by id'
    ).__dict__