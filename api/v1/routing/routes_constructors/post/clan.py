from fastapi import Depends, Body, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaClan, SaClanMembership, SaClanRequest
from models.pydantic.post import PdPostClan
from models.pydantic.returning import PdClan
from dependencies.db import get_session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from queries.patch import patch_object
from queries.create import create_object
from queries.delete import delete_objects_by_filters
from auth_bearers.v1 import Config, GetUserByJWT
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_clan_v1() -> dict:
    current_user_request = GetUserByJWT()
    entity_name = SaClan.get_table_name()

    async def _post_v1(
        clan_info: Annotated[PdPostClan, Body()],
        session: Annotated[Session, Depends(get_session)],
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
    ):
        current_user = current_user_request(jwt, session)

        sa_clan = SaClan(clanname=clan_info.clanname, owner_membership_id=None, description=clan_info.description)

        try:
            create_object(sa_clan, session)
        except IntegrityError as e:
            if 'UniqueViolation' in e.args[0]:
                raise HTTPException(409, 1)
            
            raise

        clan_membership = SaClanMembership(user_id=current_user.id, clan_id=sa_clan.id)

        try:
            create_object(clan_membership, session)
        except IntegrityError as e:
            if 'UniqueViolation' in e.args[0]:
                raise HTTPException(409, 0)

            raise

        patch_object(sa_clan, {'owner_membership_id': clan_membership.id}, session)
        delete_objects_by_filters([SaClanRequest.user_id == current_user.id], SaClanRequest, session)

        return convert_sqlalchemy_to_pydantic(sa_clan, PdClan)

    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdClan,
        responses={
            409: {'description': """
                0: User is a member of a clan
                1: Clan name is not unique 
            """}, 

            **current_user_request.responses
        },

        methods=['POST'],
        description=f'Post {entity_name}'
    ).__dict__