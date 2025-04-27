from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtPassedClanWar
from models.pydantic.returning import PdPassedClanWar
from models.sqlalchemy import SaUser, SaPassedClanWar, SaClanMembership
from sqlalchemy import ColumnElement, select

def _passed_clan_wars_get_checker_v1(
    current_user: SaUser, 
    passed_clan_war: SaPassedClanWar
) -> bool:
    all_members: list[SaClanMembership] = []

    if passed_clan_war.clan_1 is not None:
        all_members.extend(passed_clan_war.clan_1.members)

    if passed_clan_war.clan_2 is not None:
        all_members.extend(passed_clan_war.clan_2.members)

    for member in all_members:
        if member.user_id == current_user.id:
            return True
        
    return False

def _passed_clan_wars_extended_checker_v1(
    current_user: SaUser
) -> ColumnElement[bool]:
    clan_id = select(SaClanMembership.clan_id).where(SaClanMembership.user_id == current_user.id).scalar_subquery()

    return SaPassedClanWar.clan_1_id.in_(clan_id) |\
        SaPassedClanWar.clan_2_id.in_(clan_id)

passed_clan_wars_get_by_id_v1 = construct_get_by_id_route_v1(
    SaPassedClanWar, 
    PdPassedClanWar, 
    _passed_clan_wars_get_checker_v1 # type: ignore
)

passed_clan_wars_extended_get_v1 = construct_extended_get_v1(
    SaPassedClanWar,
    PdExtPassedClanWar,
    PdPassedClanWar,
    _passed_clan_wars_extended_checker_v1
)