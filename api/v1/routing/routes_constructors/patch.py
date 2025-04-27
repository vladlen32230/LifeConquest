from models.other import Route
from models.sqlalchemy import SaBase, SaUser
from models.pydantic.patch import PdPatchBase
from models.pydantic.returning import PdBase
from typing import Callable, Annotated
from dependencies.db import get_session
from dependencies.queries.get import GetObjectByIdPathV1
from fastapi import Depends, Body
from other.convertations import convert_pydantic_to_set_dict, convert_sqlalchemy_to_pydantic
from sqlalchemy.orm import Session
from queries.patch import patch_object

def construct_patch_by_id_route_v1(
    sa_entity: type[SaBase],
    pd_entity: type[PdBase],
    patch_model: type[PdPatchBase],
    permissions_checker: Callable[[SaUser, SaBase], bool]
) -> dict:
    get_object_request = GetObjectByIdPathV1(sa_entity, permissions_checker)
    status_code = 200
    entity_name = sa_entity.get_table_name()

    async def _endpoint(
        sa_instance: Annotated[SaBase, Depends(get_object_request.exc)],
        patch_info: Annotated[patch_model, Body()], # type: ignore
        session: Annotated[Session, Depends(get_session)]
    ):
        set_attributes = convert_pydantic_to_set_dict(patch_info)
        patch_object(sa_instance, set_attributes, session)

        pd_instance = convert_sqlalchemy_to_pydantic(sa_instance, pd_entity)
        return pd_instance
    
    _endpoint.__name__ = f'patch_{entity_name}_by_id_v1'

    return Route(
        f'/{entity_name}' + '/{id}',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=pd_entity,
        responses=get_object_request.responses,
        methods=['PATCH'],
        description=f'Patch {entity_name} by id'
    ).__dict__