import sys
import pathlib
sys.path.append(str(pathlib.Path().resolve()))

from other.decorators import script
from sqlalchemy.orm import Session
from queries.read import read_objects_by_filters
from models.sqlalchemy import SaUser
from other.constants import DAILY_TASK_PENALTY

@script
def score_task_update(session: Session):
    users = read_objects_by_filters([], [], SaUser, None, None, session)
    for user in users:
        user: SaUser

        user.d6 = user.d5
        user.d5 = user.d4
        user.d4 = user.d3
        user.d3 = user.d2
        user.d2 = user.d1
        user.d1 = user.d0
        user.d0 = 0

        if user.daily_task == False:
            user.score = max(0, user.score - DAILY_TASK_PENALTY)
            user.d1 -= DAILY_TASK_PENALTY

        user.daily_task = False

if __name__ == '__main__':
    score_task_update() #type: ignore