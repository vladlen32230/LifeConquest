from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDivisionMembership
from models.pydantic.returning import PdDivisionMembership
from models.sqlalchemy import SaDivisionMembership, SaUser
from sqlalchemy import ColumnElement, select

def _division_memberships_get_checker_v1(current_user: SaUser, division_membership: SaDivisionMembership):
    for membership in division_membership.division.memberships:
        if membership.user_id == current_user.id:
            return True
        
    return False

def _division_memberships_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub = select(SaDivisionMembership.division_id).where(SaDivisionMembership.user_id == current_user.id).scalar_subquery()
    return SaDivisionMembership.division_id.in_(sub)

division_memberships_get_by_id_v1 = construct_get_by_id_route_v1(
    SaDivisionMembership, 
    PdDivisionMembership, 
    _division_memberships_get_checker_v1 # type: ignore
)

division_memberships_extended_get_v1 = construct_extended_get_v1(
    SaDivisionMembership,
    PdExtDivisionMembership,
    PdDivisionMembership,
    _division_memberships_extended_checker_v1
)