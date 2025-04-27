from fastapi import Depends, Body, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaClanRequest, SaClan, SaClanMembership
from models.pydantic.post import PdPostClanMembership
from models.pydantic.returning import PdClanMembership
from dependencies.db import get_session
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from queries.read import read_object_by_filters, read_custom_stmt
from queries.create import create_object
from queries.delete import delete_objects_by_filters
from auth_bearers.v1 import Config, GetUserByJWT
from other.constants import CLAN_MAX_MEMBERS_COUNT
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_clan_membership_v1() -> dict:
    current_user_request = GetUserByJWT()
    entity_name = SaClanMembership.get_table_name()

    async def _post_v1(
        clan_membership_info: Annotated[PdPostClanMembership, Body()],
        session: Annotated[Session, Depends(get_session)],
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
    ):
        current_user = current_user_request(jwt, session)

        sa_clan = read_object_by_filters([
            SaClan.owner_membership_id == current_user.clan_membership.id
        ], SaClan, session)

        if sa_clan is None:
            raise HTTPException(404, 0)

        sa_clan_request: SaClanRequest = read_object_by_filters(
            [SaClanRequest.clan_id == sa_clan.id, SaClanRequest.user_id == clan_membership_info.user_id], 
            SaClanRequest, 
            session
        ) # type: ignore

        if sa_clan_request is None:
            raise HTTPException(404, 1)

        members_count_stmt =\
            select(func.count(SaClanMembership.id))\
            .where(SaClanMembership.clan_id == sa_clan.id)

        members_count = read_custom_stmt(members_count_stmt, session).scalar_one()

        if members_count >= CLAN_MAX_MEMBERS_COUNT:
            raise HTTPException(409)

        sa_membership = SaClanMembership(user_id=sa_clan_request.user_id, clan_id=sa_clan_request.clan_id)
        create_object(sa_membership, session)

        delete_objects_by_filters([SaClanRequest.user_id == sa_membership.user_id], SaClanRequest, session)

        return convert_sqlalchemy_to_pydantic(sa_membership, PdClanMembership)
    
    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdClanMembership,
        responses={
            404: {'description': """
                0: Clan where user is an owner has not been found
                1: Clan request to this clan from the user has not been found
            """},

            409: {'description': f'Clan is at maximum capacity of {CLAN_MAX_MEMBERS_COUNT} members'},
            **current_user_request.responses
        },

        methods=['POST'],
        description=f'Post {entity_name}. It checks for clan request to current clan from given user. If it is found, then\
            clan membership is created and request is deleted.'
    ).__dict__