import sys
import pathlib
sys.path.append(str(pathlib.Path().resolve()))

from other.decorators import script
from models.sqlalchemy import SaDivision, SaPassedDivision, SaPassedDivisionMembership
from sqlalchemy import select
from sqlalchemy.orm import Session
from queries.read import read_custom_stmt
from queries.create import create_object
from queries.delete import delete_object

@script
def end_divisions(session: Session):
    for current_division in read_custom_stmt(select(SaDivision), session).scalars():
        current_division: SaDivision = current_division

        passed_division = SaPassedDivision()
        create_object(passed_division, session)

        for current_participant in current_division.memberships:
            passed_division_participant = SaPassedDivisionMembership(
                user_id=current_participant.user_id, 
                passed_division_id=passed_division.id, 
                score=current_participant.score
            )

            create_object(passed_division_participant, session)

        delete_object(current_division, session)
            
if __name__ == '__main__':
    end_divisions() # type: ignore