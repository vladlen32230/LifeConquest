from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtClanWarInvite
from models.pydantic.returning import PdClanWarInvite
from models.sqlalchemy import SaClanWarInvite, SaUser

def clan_war_invites_delete_checker_v1(current_user: SaUser, clan_war_invite: SaClanWarInvite) -> bool:
    return current_user.clan_membership is not None and\
    current_user.clan_membership.id == clan_war_invite.clan.owner_membership_id

clan_war_invites_get_by_id_v1 = construct_get_by_id_route_v1(SaClanWarInvite, PdClanWarInvite)
clan_war_invites_extended_get_v1 = construct_extended_get_v1(SaClanWarInvite, PdExtClanWarInvite, PdClanWarInvite)

clan_war_invites_delete_by_id_v1 = construct_delete_by_id_route_v1(
    SaClanWarInvite, 
    clan_war_invites_delete_checker_v1 # type: ignore
)