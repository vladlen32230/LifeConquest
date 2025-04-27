from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDivisionMembership
from models.pydantic.returning import PdPassedDivisionMembership
from models.sqlalchemy import SaPassedDivisionMembership, SaUser
from sqlalchemy import ColumnElement, select

def _passed_division_memberships_get_checker_v1(
    current_user: SaUser, 
    passed_division_membership: SaPassedDivisionMembership
):
    for membership in passed_division_membership.passed_division.memberships:
        if membership.user_id == current_user.id:
            return True

    return False

def _passed_division_memberships_extended_checker_v1(
    current_user: SaUser
) -> ColumnElement[bool]:
    sub = select(
        SaPassedDivisionMembership.passed_division_id
    ).where(
        SaPassedDivisionMembership.user_id == current_user.id
    ).scalar_subquery()
    
    return SaPassedDivisionMembership.passed_division_id.in_(sub)

passed_division_memberships_get_by_id_v1 = construct_get_by_id_route_v1(
    SaPassedDivisionMembership, 
    PdPassedDivisionMembership, 
    _passed_division_memberships_get_checker_v1 # type: ignore
)

passed_division_memberships_extended_get_v1 = construct_extended_get_v1(
    SaPassedDivisionMembership,
    PdExtDivisionMembership,
    PdPassedDivisionMembership,
    _passed_division_memberships_extended_checker_v1
)