from fastapi import Depends, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaClan, SaClanWarInvite, SaUser, SaClanMembership, SaClanWar, SaClanWarParticipant
from models.pydantic.returning import PdClanWar, PdClanWarInvite, PdClanWarPostResponseModel
from dependencies.db import get_session
from sqlalchemy import func, select, between
from sqlalchemy.orm import Session
from queries.read import read_object_by_filters, exist_objects_by_fiters, read_custom_stmt
from queries.create import create_object
from queries.delete import delete_object_by_id
from auth_bearers.v1 import Config, GetUserByJWT
from other.constants import CLAN_WAR_ABSOLUTE_SCORE_DELTA, CLAN_WAR_RELATIVE_SCORE_DELTA, CLAN_WAR_AVERAGE_WEEK_SCORE_ABSOLUTE_DELTA
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_clan_war_v1() -> dict:
    current_user_request = GetUserByJWT()
    entity_name = SaClanWar.get_table_name()

    async def _post_v1(
        session: Annotated[Session, Depends(get_session)],
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
    ):
        current_user = current_user_request(jwt, session)

        current_clan: SaClan = read_object_by_filters([
            SaClan.owner_membership_id == SaClanMembership.id, 
            SaClanMembership.user_id == current_user.id
        ], SaClan, session) #type: ignore

        if current_clan is None:
            raise HTTPException(404)
        
        if exist_objects_by_fiters(
            [(SaClanWar.clan_1_id == current_clan.id) | (SaClanWar.clan_2_id == current_clan.id)], 
            SaClanWar, session
        ):
            raise HTTPException(409, 0)
        
        if exist_objects_by_fiters([SaClanWarInvite.clan_id == current_clan.id], SaClanWarInvite, session):
            raise HTTPException(409, 1)
        
        score_sum_alias = func.sum(SaUser.score)
        membership_count_alias = func.count(SaUser.id)

        week_score_sum_alias = (
            func.sum(SaUser.d0) + 
            func.sum(SaUser.d1) + 
            func.sum(SaUser.d2) + 
            func.sum(SaUser.d3) +
            func.sum(SaUser.d4) + 
            func.sum(SaUser.d5) +
            func.sum(SaUser.d6)
        )

        current_stmt = select(
            score_sum_alias, 
            week_score_sum_alias,
            membership_count_alias
        ).where(
            (SaClanMembership.clan_id == current_clan.id) & (SaClanMembership.user_id == SaUser.id)
        )

        current_score_sum, current_week_score_sum, current_member_count = read_custom_stmt(
            current_stmt, 
            session
        ).first() # type: ignore

        stmt = \
            select(
                SaClanWarInvite.id, SaClan
            ).where(
                SaClanWarInvite.clan_id == SaClan.id,
                SaClanMembership.clan_id == SaClan.id,
                SaClanMembership.user_id == SaUser.id,
            ).group_by(
                SaClan.id, SaClanWarInvite.id
            ).having(
                membership_count_alias == current_member_count, 
                between(
                    score_sum_alias,
                    (current_score_sum - CLAN_WAR_ABSOLUTE_SCORE_DELTA) // CLAN_WAR_RELATIVE_SCORE_DELTA,
                    (current_score_sum + CLAN_WAR_ABSOLUTE_SCORE_DELTA) * CLAN_WAR_RELATIVE_SCORE_DELTA
                ),

                between(
                    week_score_sum_alias, 
                    current_week_score_sum//current_member_count - CLAN_WAR_AVERAGE_WEEK_SCORE_ABSOLUTE_DELTA, 
                    current_week_score_sum//current_member_count + CLAN_WAR_AVERAGE_WEEK_SCORE_ABSOLUTE_DELTA
                )
            ).order_by(func.random())

        res = read_custom_stmt(stmt, session).first()

        if res is None:
            clan_war_invite = SaClanWarInvite(clan_id=current_clan.id)
            create_object(clan_war_invite, session)

            pd_clan_war_invite = convert_sqlalchemy_to_pydantic(clan_war_invite, PdClanWarInvite)

            return PdClanWarPostResponseModel(
                clan_war_started=False, 
                model=pd_clan_war_invite # type: ignore
            )
        else:
            invite_id: int = res[0]
            other_clan: SaClan = res[1]

            clan_war = SaClanWar(clan_1_id=other_clan.id, clan_2_id=current_clan.id)
            create_object(clan_war, session)

            for member in current_clan.members:
                create_object(SaClanWarParticipant(
                    user_membership_id=member.id, 
                    user_id=member.user_id,
                    clan_war_id=clan_war.id, 
                    clan_id=current_clan.id
                ), session)
            
            for member in other_clan.members:
                create_object(SaClanWarParticipant(
                    user_membership_id=member.id, 
                    user_id=member.user_id,
                    clan_war_id=clan_war.id, 
                    clan_id=other_clan.id
                ), session)

            delete_object_by_id(invite_id, SaClanWarInvite, session)

            pd_clan_war = convert_sqlalchemy_to_pydantic(clan_war, PdClanWar)

            return PdClanWarPostResponseModel(
                clan_war_started=True, 
                model=pd_clan_war #type: ignore
            )

    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdClanWarPostResponseModel,
        responses={
            404: {'description': "Clan where user is an owner has not been found"},
            409: {'description': """
                0: Clan is currently in a clan war
                1: Clan already has clan war invite
            """},

            **current_user_request.responses
        },

        methods=['POST'],
        description=f'Post {entity_name}. It checks clan war invites to find suitable enemy clan. If at least 1 is found, then\
            clan war is created and invite is deleted. If suitable clan is not found, then clan war invite is created'
    ).__dict__