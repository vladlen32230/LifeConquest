from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtPassedDivision
from models.pydantic.returning import PdPassedDivision
from models.sqlalchemy import SaPassedDivision, SaUser, SaPassedDivisionMembership
from sqlalchemy import ColumnElement, select

def _passed_divisions_get_checker_v1(current_user: SaUser, passed_division: SaPassedDivision) -> bool:
    for membership in passed_division.memberships:
        if membership.user_id == current_user.id:
            return True
    
    return False

def _passed_divisions_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub = select(
        SaPassedDivisionMembership.passed_division_id
    ).where(
        SaPassedDivisionMembership.user_id == current_user.id
    ).scalar_subquery()
    
    return SaPassedDivision.id.in_(sub)

passed_divisions_get_by_id_v1 = construct_get_by_id_route_v1(
    SaPassedDivision, 
    PdPassedDivision, 
    _passed_divisions_get_checker_v1 # type: ignore
)

passed_divisions_extended_get_v1 = construct_extended_get_v1(
    SaPassedDivision,
    PdExtPassedDivision,
    PdPassedDivision,
    _passed_divisions_extended_checker_v1
)