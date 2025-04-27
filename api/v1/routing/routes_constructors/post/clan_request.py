from fastapi import Depends, Body, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaClanRequest, SaClan, SaClanMembership
from models.pydantic.post import PdPostClanRequest
from models.pydantic.returning import PdClanRequest
from dependencies.db import get_session
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from queries.read import exist_objects_by_fiters, read_object_by_id, read_custom_stmt
from queries.create import create_object
from auth_bearers.v1 import Config, GetUserByJWT
from other.constants import CLAN_MAX_MEMBERS_COUNT
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_clan_request_v1() -> dict:
    current_user_request = GetUserByJWT()
    entity_name = SaClanRequest.get_table_name()

    async def _post_v1(
        clan_request_info: Annotated[PdPostClanRequest, Body()],
        session: Annotated[Session, Depends(get_session)],
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
    ):
        current_user = current_user_request(jwt, session)

        if exist_objects_by_fiters([SaClanMembership.user_id == current_user.id], SaClanMembership, session):
            raise HTTPException(409, 1)

        sa_clan: SaClan = read_object_by_id(clan_request_info.clan_id, SaClan, session) # type: ignore
        if sa_clan is None:
            raise HTTPException(404)
        
        if sa_clan.recruiting is False:
            raise HTTPException(409, 2)
        
        members_count_stmt = select(func.count(SaClanMembership.user_id)).where(SaClanMembership.clan_id == sa_clan.id)
        members_count = read_custom_stmt(members_count_stmt, session).scalar_one_or_none()

        if not members_count or members_count >= CLAN_MAX_MEMBERS_COUNT:
            raise HTTPException(409, 3)

        sa_clan_request = SaClanRequest(user_id=current_user.id, clan_id=clan_request_info.clan_id)
        
        try:
            create_object(sa_clan_request, session)
        except IntegrityError as e:
            if 'ForeignKeyViolation' in e.args[0]:
                raise HTTPException(404)
            if 'UniqueViolation' in e.args[0]:
                raise HTTPException(409, 0)
            
            raise

        return convert_sqlalchemy_to_pydantic(sa_clan_request, PdClanRequest)
    
    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdClanRequest,
        responses={
            409: {'description': f"""
                0: User has already sent request to this clan
                1: User is a member of a clan
                2: Clan is not recruiting members
                3: Clan already has maximum of {CLAN_MAX_MEMBERS_COUNT} members
            """}, 

            404: {'description': 'Clan does not exist'},
            **current_user_request.responses
        },

        methods=['POST'],
        description=f'Post {entity_name}'
    ).__dict__