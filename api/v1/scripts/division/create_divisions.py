import sys
import pathlib
import math
sys.path.append(str(pathlib.Path().resolve()))

from other.constants import DIVISION_THRESHOLD_SCORE, DIVISION_MAX_PARTICIPANTS_COUNT
from other.decorators import script
from models.sqlalchemy import SaUser, SaDivision, SaDivisionMembership
from sqlalchemy import select, func, case
from sqlalchemy.orm import Session
from queries.read import read_custom_stmt
from queries.create import create_object

@script
def create_divisions(session: Session):
    stmt = select(
        func.coalesce(func.sum(case((SaUser.score < DIVISION_THRESHOLD_SCORE, 1), else_=0)), 0),
        func.coalesce(func.sum(case((SaUser.score >= DIVISION_THRESHOLD_SCORE, 1), else_=0)), 0)
    ).where(SaUser.participate_division == True)

    result = read_custom_stmt(stmt, session).first()
    below_threshold_count, above_threshold_count = result # type: ignore

    above_threshold_teams_count = math.ceil(above_threshold_count / DIVISION_MAX_PARTICIPANTS_COUNT)
    below_threshold_teams_count = math.ceil(below_threshold_count / DIVISION_MAX_PARTICIPANTS_COUNT)

    above_threshold_users: list[SaUser] = []
    below_threshold_users: list[SaUser] = []

    above_threshold_current_division_capacity, below_threshold_current_division_capacity =\
        round(above_threshold_count / max(above_threshold_teams_count, 1)),\
        round(below_threshold_count / max(below_threshold_teams_count, 1))
    
    def create_division(users: list[SaUser], session: Session) -> None:
        sa_division = SaDivision()
        create_object(sa_division, session)

        for current_division_user in users:
            division_membership = SaDivisionMembership(user_id=current_division_user.id, division_id=sa_division.id)
            create_object(division_membership, session)

    def recalculate_count_capacity(current_users_count: int, current_capacity: int, current_teams_count) -> tuple[int, int]:
        current_users_count = current_users_count - current_capacity
        current_capacity = round(current_users_count / max(current_teams_count, 1))
        return (current_users_count, current_capacity)

    users = read_custom_stmt(
        select(
            SaUser
        ).where(
            SaUser.participate_division == True
        ).order_by(
            SaUser.d0 + SaUser.d1 + SaUser.d2 + SaUser.d3 + SaUser.d4 + SaUser.d5 + SaUser.d6,
            SaUser.score
        ), session)
    
    for user in users.scalars():
        user: SaUser = user
        
        if user.score < 200:
            below_threshold_users.append(user)

            if len(below_threshold_users) == below_threshold_current_division_capacity:
                create_division(below_threshold_users, session)
                below_threshold_users.clear()

                below_threshold_teams_count -= 1
                below_threshold_count, below_threshold_current_division_capacity =\
                    recalculate_count_capacity(
                        below_threshold_count, 
                        below_threshold_current_division_capacity, 
                        below_threshold_teams_count
                    )
        else:
            above_threshold_users.append(user)

            if len(above_threshold_users) == above_threshold_current_division_capacity:
                create_division(above_threshold_users, session)

                above_threshold_users.clear()

                above_threshold_teams_count -= 1
                above_threshold_count, above_threshold_current_division_capacity =\
                    recalculate_count_capacity(
                        above_threshold_count, 
                        above_threshold_current_division_capacity,
                        above_threshold_teams_count
                    )

if __name__ == '__main__':
    create_divisions() # type: ignore