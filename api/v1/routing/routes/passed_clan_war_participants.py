from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtPassedClanWarParticipant
from models.pydantic.returning import PdPassedClanWarParticipant
from models.sqlalchemy import SaUser, SaPassedClanWarParticipant, SaClanMembership, SaPassedClanWar
from sqlalchemy import ColumnElement, select

def _passed_clan_war_participants_get_checker_v1(
    current_user: SaUser, 
    passed_clan_war_participant: SaPassedClanWarParticipant
) -> bool:
    passed_clan_war = passed_clan_war_participant.passed_clan_war
    all_members: list[SaClanMembership] = []

    if passed_clan_war.clan_1 is not None:
        all_members.extend(passed_clan_war.clan_1.members)

    if passed_clan_war.clan_2 is not None:
        all_members.extend(passed_clan_war.clan_2.members)

    for member in all_members:
        if member.user_id == current_user.id:
            return True
        
    return False

def _passed_clan_war_participants_extended_checker_v1(
    current_user: SaUser
) -> ColumnElement[bool]:
    current_clan_id = select(SaClanMembership.clan_id).where(SaClanMembership.user_id == current_user.id).scalar_subquery()

    clan_war_ids = select(SaPassedClanWar.id).where(
        SaPassedClanWar.clan_1_id.in_(current_clan_id) | 
        SaPassedClanWar.clan_2_id.in_(current_clan_id)
    ).scalar_subquery()

    return SaPassedClanWarParticipant.passed_clan_war_id.in_(clan_war_ids)

passed_clan_war_participant_get_by_id_v1 = construct_get_by_id_route_v1(
    SaPassedClanWarParticipant, 
    PdPassedClanWarParticipant, 
    _passed_clan_war_participants_get_checker_v1 # type: ignore
)

passed_clan_war_participants_extended_get_v1 = construct_extended_get_v1(
    SaPassedClanWarParticipant,
    PdExtPassedClanWarParticipant,
    PdPassedClanWarParticipant,
    _passed_clan_war_participants_extended_checker_v1
)