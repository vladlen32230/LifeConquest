from fastapi import Depends, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaDuelInvite, SaUser, SaDuel
from models.pydantic.returning import PdDuel, PdDuelInvite, PdDuelPostResponseModel
from dependencies.db import get_session
from sqlalchemy import func, select, between, or_
from sqlalchemy.orm import Session
from queries.read import read_object_by_filters, exist_objects_by_fiters
from queries.create import create_object
from queries.delete import delete_object
from auth_bearers.v1 import Config, GetUserByJWT
from other.constants import DUEL_ABSOLUTE_SCORE_DELTA, DUEL_RELATIVE_SCORE_DELTA, DUEL_THRESHOLD_SCORE, DUEL_WEEK_SCORE_ABSOLUTE_DELTA
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_duel_v1() -> dict:
    current_user_request = GetUserByJWT()
    entity_name = SaDuel.get_table_name()

    async def _post_v1(
        session: Annotated[Session, Depends(get_session)],
        jwt: Annotated[str | None, Depends(Config.oauth2_scheme)]
    ):
        current_user = current_user_request(jwt, session)

        if exist_objects_by_fiters([
            or_(
                SaDuel.user_1_id == current_user.id, 
                SaDuel.user_2_id == current_user.id
            )
        ], SaDuel, session):
            raise HTTPException(409, 0)
        
        if exist_objects_by_fiters([
            SaDuelInvite.user_id == current_user.id
        ], SaDuelInvite, session):
            raise HTTPException(409, 1)

        week_score = sum(
            [
                current_user.d0, 
                current_user.d1, 
                current_user.d2, 
                current_user.d3, 
                current_user.d4, 
                current_user.d5, 
                current_user.d6
            ]
        )

        left_border_score = 0 if current_user.score < DUEL_THRESHOLD_SCORE else\
            max(DUEL_THRESHOLD_SCORE, (current_user.score - DUEL_ABSOLUTE_SCORE_DELTA) // DUEL_RELATIVE_SCORE_DELTA)
        right_border_score = DUEL_THRESHOLD_SCORE if current_user.score < DUEL_THRESHOLD_SCORE else\
            (current_user.score + DUEL_ABSOLUTE_SCORE_DELTA) * DUEL_RELATIVE_SCORE_DELTA

        sub = select(SaUser.id).where(
            between(
                SaUser.d0 + SaUser.d1 + SaUser.d2 + SaUser.d3 + SaUser.d4 + SaUser.d5 + SaUser.d6,
                week_score - DUEL_WEEK_SCORE_ABSOLUTE_DELTA, 
                week_score + DUEL_WEEK_SCORE_ABSOLUTE_DELTA
            ),

            between(SaUser.score, left_border_score, right_border_score)
        )

        invite: SaDuelInvite = read_object_by_filters(
            [SaDuelInvite.user_id.in_(sub.scalar_subquery())],
            SaDuelInvite,
            session,
            [func.random()]
        ) # type: ignore

        if invite is None:
            sa_new_invite = SaDuelInvite(user_id=current_user.id)
            create_object(sa_new_invite, session)

            pd_new_invite = convert_sqlalchemy_to_pydantic(sa_new_invite, PdDuelInvite)

            return PdDuelPostResponseModel(
                duel_started=False, 
                model=pd_new_invite
            )
        else:
            sa_duel = SaDuel(user_1_id=invite.user_id, user_2_id=current_user.id)

            create_object(sa_duel, session)
            delete_object(invite, session)

            pd_duel = convert_sqlalchemy_to_pydantic(sa_duel, PdDuel)
            
            return PdDuelPostResponseModel(
                duel_started=True, 
                model=pd_duel #type: ignore
            )
        
    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdDuelPostResponseModel,
        responses={
            409: {'description': """
                0: User is currently participating in a duel
                1: User already has waiting invite
            """},

            **current_user_request.responses
        },

        methods=['POST'],
        description=f'Post {entity_name}. It checks current duel invites for suitable enemy. If at least 1 is found, then\
            duel is created and invite is deleted. If suitable enemy is not found, then duel invite is created'
    ).__dict__