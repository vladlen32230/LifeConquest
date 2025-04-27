from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtClanMembership
from models.pydantic.returning import PdClanMembership
from models.sqlalchemy import SaClanMembership, SaUser

def _clan_memberships_delete_checker_v1(current_user: SaUser, clan_membership: SaClanMembership) -> bool:
    return current_user.id == clan_membership.user_id or\
    current_user.clan_membership is not None and\
    current_user.clan_membership.id == clan_membership.clan.owner_membership_id

clan_memberships_get_by_id_v1 = construct_get_by_id_route_v1(SaClanMembership, PdClanMembership)
clan_memberships_delete_by_id_v1 = construct_delete_by_id_route_v1(
    SaClanMembership, 
    _clan_memberships_delete_checker_v1 # type: ignore
)

clan_memberships_extended_get_v1 = construct_extended_get_v1(SaClanMembership, PdExtClanMembership, PdClanMembership)