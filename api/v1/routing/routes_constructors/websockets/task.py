from fastapi import WebSocket, Query, Depends, HTTPException
from fastapi.websockets import WebSocketDisconnect
from typing import Annotated
from auth_bearers.v1 import GetUserByJWT
from sqlalchemy.orm import Session
from dependencies.db import get_session
from other.constants import TASK_MIN_MINUTES, TASK_MAX_MINUTES
from queries.patch import update_objects_values
from models.sqlalchemy import SaDuel, SaClanWarParticipant, SaDivisionMembership
import asyncio

def construct_task_websocket_v1() -> dict:
    user_request = GetUserByJWT()

    async def _create_task(
        websocket: WebSocket, 
        jwt: Annotated[str, Query()], 
        time: Annotated[int, Query(ge=TASK_MIN_MINUTES, le=TASK_MAX_MINUTES)], 
        session: Annotated[Session, Depends(get_session)]
    ):
        await websocket.accept()

        try:
            sa_user = user_request(jwt, session)
        except HTTPException:
            await websocket.close(3000)
            return

        if sa_user.occupied:
            await websocket.close(3003)
            return
        
        sa_user.occupied = True
        session.commit()

        try:
            for _ in range(time):
                await asyncio.sleep(60)
                
            await websocket.send_text('ping')
        except:
            pass

        else:
            await websocket.close()

            sa_user.daily_task = True
            sa_user.d0 += time
            sa_user.score += time

            update_objects_values(SaDuel, [SaDuel.user_1_id == sa_user.id], {'user_1_score': SaDuel.user_1_score + time}, session)
            update_objects_values(SaDuel, [SaDuel.user_2_id == sa_user.id], {'user_2_score': SaDuel.user_2_score + time}, session)

            update_objects_values(
                SaClanWarParticipant, 
                [SaClanWarParticipant.user_id == sa_user.id], 
                {'score': SaClanWarParticipant.score + time}, 
                session
            )

            update_objects_values(
                SaDivisionMembership, 
                [SaDivisionMembership.user_id == sa_user.id], 
                {'score': SaDivisionMembership.score + time}, 
                session
            )
        
        finally:
            sa_user.occupied = False

            try:
                await websocket.close(1011)
            except RuntimeError:
                pass

    return {
        'path': '/task',
        'endpoint': _create_task
    }