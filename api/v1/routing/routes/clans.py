from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.delete import construct_delete_by_id_route_v1
from routing.routes_constructors.patch import construct_patch_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from routing.routes_constructors.post.clan import construct_post_clan_v1
from models.pydantic.patch import PdPatchClan
from models.pydantic.extended import PdExtClan
from models.pydantic.returning import PdClan
from models.sqlalchemy import SaClan, SaUser

def _clans_delete_patch_checker_v1(current_user: SaUser, clan: SaClan):
    return current_user.clan_membership is not None and\
    clan.owner_membership_id == current_user.clan_membership.id

clans_get_by_id_v1 = construct_get_by_id_route_v1(SaClan, PdClan)
clans_delete_by_id_v1 = construct_delete_by_id_route_v1(SaClan, _clans_delete_patch_checker_v1) # type: ignore
clans_patch_by_id_v1 = construct_patch_by_id_route_v1(SaClan, PdClan, PdPatchClan, _clans_delete_patch_checker_v1) # type: ignore
clans_extended_get_v1 = construct_extended_get_v1(SaClan, PdExtClan, PdClan)
clans_post_v1 = construct_post_clan_v1()