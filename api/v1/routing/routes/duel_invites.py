from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDuelInvite
from models.pydantic.returning import PdDuelInvite
from models.sqlalchemy import SaDuelInvite, SaUser

def _duel_invite_delete_checker_v1(current_user: SaUser, duel_invite: SaDuelInvite) -> bool:
    return current_user.id == duel_invite.user_id

duel_invites_get_by_id_v1 = construct_get_by_id_route_v1(SaDuelInvite, PdDuelInvite)
duel_invites_extended_get_v1 = construct_extended_get_v1(
    SaDuelInvite,
    PdExtDuelInvite,
    PdDuelInvite
)

duel_invites_delete_by_id_v1 = construct_delete_by_id_route_v1(SaDuelInvite, _duel_invite_delete_checker_v1) # type: ignore