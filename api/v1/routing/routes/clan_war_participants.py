from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtClanWarParticipant
from models.pydantic.returning import PdClanWarParticipant
from models.sqlalchemy import SaUser, SaClanWarParticipant, SaClanMembership, SaClanWar
from sqlalchemy import ColumnElement, select

def _clan_war_participants_get_checker_v1(current_user: SaUser, clan_war_participant: SaClanWarParticipant) -> bool:
    clan_war = clan_war_participant.clan_war
    all_members = [*clan_war.clan_1.members, *clan_war.clan_2.members]
    for member in all_members:
        if member.user_id == current_user.id:
            return True
        
    return False

def _clan_war_participants_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    sub1 = select(SaClanMembership.clan_id).where(SaClanMembership.user_id == current_user.id).scalar_subquery()
    sub2 = select(SaClanWar.id).where(SaClanWar.clan_1_id.in_(sub1) | SaClanWar.clan_2_id.in_(sub1)).scalar_subquery()
    return SaClanWarParticipant.clan_war_id.in_(sub2)

clan_war_participants_get_by_id_v1 = construct_get_by_id_route_v1(
    SaClanWarParticipant, 
    PdClanWarParticipant, 
    _clan_war_participants_get_checker_v1 # type: ignore
)

clan_war_participants_extended_get_v1 = construct_extended_get_v1(
    SaClanWarParticipant,
    PdExtClanWarParticipant,
    PdClanWarParticipant,
    _clan_war_participants_extended_checker_v1
)