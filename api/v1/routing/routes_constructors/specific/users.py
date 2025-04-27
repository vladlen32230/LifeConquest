from auth_bearers.v1 import GetUserByJWT, Config
from typing import Annotated
from fastapi import Depends
from dependencies.db import get_session
from sqlalchemy.orm import Session
from models.other import Route
from models.sqlalchemy import (
    SaUser, 
    SaClanMembership, 
    SaClan, 
    SaDuel, 
    SaDivision, 
    SaDivisionMembership, 
    SaClanWar, 
    SaClanWarParticipant
)

from models.pydantic.returning import (
    PdUser, 
    PdUserInfo, 
    PdClanMembership, 
    PdClan, 
    PdDuel, 
    PdDivisionMembership, 
    PdDivision, 
    PdClanWar,
    PdClanWarParticipant
)

from other.convertations import convert_sqlalchemy_to_pydantic
from queries.read import read_object_by_filters

def construct_get_user_by_jwt_route_v1() -> dict:
    get_user_request = GetUserByJWT()
    entity_name = SaUser.get_table_name()
    pd_entity = PdUser
    status_code = 200

    async def _endpoint(
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)],
        session: Annotated[Session, Depends(get_session)]
    ):
        sa_user = get_user_request(jwt, session)
        return convert_sqlalchemy_to_pydantic(sa_user, pd_entity)

    _endpoint.__name__ = f'get_{entity_name}_by_jwt_v1'

    return Route(
        path=f'/current_user',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=pd_entity,
        responses=get_user_request.responses,
        methods=['GET'],
        description=f'Get {entity_name} object by authorization header with JWT'
    ).__dict__

def construct_get_user_info_route_v1() -> dict:
    get_user_request = GetUserByJWT()
    status_code = 200

    async def _endpoint(
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)],
        session: Annotated[Session, Depends(get_session)]
    ):
        sa_user: SaUser = get_user_request(jwt, session)

        clan_membership: SaClanMembership | None = read_object_by_filters(
            [SaClanMembership.user_id == sa_user.id],
            SaClanMembership,
            session
        ) # type: ignore

        clan = None if clan_membership is None else read_object_by_filters(
            [SaClan.id == clan_membership.clan_id],
            SaClan,
            session
        )

        division_membership: SaDivisionMembership | None = read_object_by_filters(
            [SaDivisionMembership.user_id == sa_user.id],
            SaDivisionMembership,
            session
        ) # type: ignore

        division = None if division_membership is None else read_object_by_filters(
            [SaDivision.id == SaDivisionMembership.division_id],
            SaDivision,
            session
        )

        duel = read_object_by_filters(
            [(SaDuel.user_1_id == sa_user.id) | (SaDuel.user_2_id == sa_user.id)],
            SaDuel,
            session
        )

        clan_war_participant: SaClanWarParticipant | None = read_object_by_filters(
            [SaClanWarParticipant.user_id == sa_user.id],
            SaClanWarParticipant,
            session
        ) # type: ignore

        clan_war = None if clan_war_participant is None else read_object_by_filters(
            [SaClanWar.id == clan_war_participant.clan_war_id],
            SaClanWar,
            session
        )
        
        return PdUserInfo(
            user=convert_sqlalchemy_to_pydantic(sa_user, PdUser),# type: ignore
            clan=convert_sqlalchemy_to_pydantic(clan, PdClan),# type: ignore
            clan_membership=convert_sqlalchemy_to_pydantic(clan_membership, PdClanMembership),# type: ignore
            division=convert_sqlalchemy_to_pydantic(division, PdDivision),# type: ignore
            division_membership=convert_sqlalchemy_to_pydantic(division_membership, PdDivisionMembership),# type: ignore
            duel=convert_sqlalchemy_to_pydantic(duel, PdDuel),# type: ignore
            clan_war=convert_sqlalchemy_to_pydantic(clan_war, PdClanWar),# type: ignore
            clan_war_participant=convert_sqlalchemy_to_pydantic(clan_war_participant, PdClanWarParticipant)# type: ignore
        )

    _endpoint.__name__ = f'get_user_info_by_jwt_v1'

    return Route(
        path=f'/current_user_info',
        endpoint=_endpoint,
        status_code=status_code,
        response_model=PdUserInfo,
        responses=get_user_request.responses,
        methods=['GET'],
        description=f'Get current user\'s extended info'
    ).__dict__