from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from routing.routes_constructors.post.clan_request import construct_post_clan_request_v1
from models.pydantic.returning import PdClanRequest
from models.pydantic.extended import PdExtClanRequest
from models.sqlalchemy import SaClanRequest, SaUser, SaClan
from sqlalchemy import ColumnElement, or_, select

def _clan_requests_get_delete_checker_v1(current_user: SaUser, clan_request: SaClanRequest) -> bool:
    return current_user.clan_membership is not None and\
    clan_request.clan.owner_membership_id == current_user.clan_membership.id or\
    clan_request.user_id == current_user.id

def _clan_requests_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub = select(SaClan.id).where(SaClan.owner_membership_id == current_user.clan_membership.id).scalar_subquery()
    return or_(SaClanRequest.user_id == current_user.id, SaClanRequest.clan_id.in_(sub))

clan_requests_get_by_id_v1 = construct_get_by_id_route_v1(
    SaClanRequest, 
    PdClanRequest, 
    _clan_requests_get_delete_checker_v1 # type: ignore
)

clan_requests_delete_by_id_v1 = construct_delete_by_id_route_v1(
    SaClanRequest, 
    _clan_requests_get_delete_checker_v1 # type: ignore
)

clan_requests_extended_get_v1 = construct_extended_get_v1(
    SaClanRequest, 
    PdExtClanRequest, 
    PdClanRequest, 
    _clan_requests_extended_checker_v1
)

clans_requests_post_v1 = construct_post_clan_request_v1()