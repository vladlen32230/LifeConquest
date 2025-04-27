from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtClanWar
from models.pydantic.returning import PdClanWar
from models.sqlalchemy import SaClanWar, SaUser, SaClanMembership
from sqlalchemy import ColumnElement, select, or_

def _clan_wars_get_checker_v1(current_user: SaUser, clan_war: SaClanWar) -> bool:
    all_members = [*clan_war.clan_1.members, *clan_war.clan_2.members]
    for member in all_members:
        if member.user_id == current_user.id:
            return True

    return False

def _clan_wars_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub = select(SaClanMembership.clan_id).where(SaClanMembership.user_id == current_user.id).scalar_subquery()
    return or_(
        SaClanWar.clan_1_id.in_(sub), 
        SaClanWar.clan_2_id.in_(sub),
    )

clan_wars_get_by_id_v1 = construct_get_by_id_route_v1(SaClanWar, PdClanWar, _clan_wars_get_checker_v1) # type: ignore
clan_wars_extended_get_v1 = construct_extended_get_v1(SaClanWar, PdExtClanWar, PdClanWar, _clan_wars_extended_checker_v1)