import sys
import pathlib
sys.path.append(str(pathlib.Path().resolve()))

from other.decorators import script
from models.sqlalchemy import SaDuel, SaPassedDuel, SaUser
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from other.constants import DUEL_TIME_SPAN
from queries.read import read_custom_stmt, read_object_by_id
from queries.create import create_object
from queries.delete import delete_object

@script
def check_duels_time_span(session: Session):
    for duel in read_custom_stmt(select(SaDuel).where(
        SaDuel.started_at + DUEL_TIME_SPAN < datetime.now()
    ), session).scalars():
        duel: SaDuel = duel
        passed_duel = SaPassedDuel(
            user_1_id=duel.user_1_id, 
            user_2_id=duel.user_2_id, 
            user_1_score=duel.user_1_score, 
            user_2_score=duel.user_2_score
        )

        user_1: SaUser = read_object_by_id(duel.user_1_id, SaUser, session)
        user_2: SaUser = read_object_by_id(duel.user_2_id, SaUser, session)
        difference =  abs(duel.user_1_score - duel.user_2_score)

        if duel.user_1_score > duel.user_2_score:
            user_1.score = user_1.score + difference
            user_1.d0 = user_1.d0 + difference

            user_2.score = max(0, user_2.score - difference)
            user_2.d0 = user_2.d0 - difference

        elif duel.user_2_score > duel.user_1_score:
            user_2.score = user_2.score + difference
            user_2.d0 = user_2.d0 + difference

            user_1.score = max(0, user_1.score - difference)
            user_1.d0 = user_1.d0 - difference

        create_object(passed_duel, session)
        delete_object(duel, session)

if __name__ == '__main__':
    check_duels_time_span() #type: ignore