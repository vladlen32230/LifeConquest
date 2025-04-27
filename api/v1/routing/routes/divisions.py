from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDivision
from models.pydantic.returning import PdDivision
from models.sqlalchemy import SaDivision, SaUser, SaDivisionMembership
from sqlalchemy import ColumnElement, select

def _divisions_get_checker_v1(current_user: SaUser, division: SaDivision) -> bool:
    for membership in division.memberships:
        if membership.user_id == current_user.id:
            return True

    return False

def _divisions_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub = select(SaDivisionMembership.division_id).where(SaDivisionMembership.user_id == current_user.id).scalar_subquery()
    return SaDivision.id.in_(sub)

divisions_get_by_id_v1 = construct_get_by_id_route_v1(SaDivision, PdDivision, _divisions_get_checker_v1) # type: ignore
divisions_extended_get_v1 = construct_extended_get_v1(
    SaDivision, 
    PdExtDivision, 
    PdDivision, 
    _divisions_extended_checker_v1, 
)