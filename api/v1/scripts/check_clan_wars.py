import sys
import pathlib
sys.path.append(str(pathlib.Path().resolve()))

from other.decorators import script
from models.sqlalchemy import SaClanWar, SaPassedClanWar, SaPassedClanWarParticipant
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from other.constants import CLAN_WAR_TIME_SPAN
from queries.read import read_custom_stmt
from queries.create import create_object
from queries.delete import delete_object

@script
def check_clan_wars_time_span(session: Session):
    for clan_war in read_custom_stmt(select(SaClanWar).where(
        SaClanWar.started_at + CLAN_WAR_TIME_SPAN < datetime.now()
    ), session).scalars():
        clan_war: SaClanWar = clan_war

        current_participants = clan_war.participants

        passed_clan_war = SaPassedClanWar(clan_1_id=clan_war.clan_1_id, clan_2_id=clan_war.clan_2_id)
        create_object(passed_clan_war, session)

        clan_ids_score = [
            [None, 0],
            [None, 0]
        ]

        members_count = 0

        for current_participant in current_participants:
            if clan_ids_score[0][0] is None or clan_ids_score[0][0] == current_participant.clan_id:
                clan_ids_score[0][0] = current_participant.clan_id
                clan_ids_score[0][1] += current_participant.score

            else:
                clan_ids_score[1][0] = current_participant.clan_id
                clan_ids_score[1][1] += current_participant.score

            members_count += 1

        winner = clan_ids_score[0][0] if clan_ids_score[0][1] > clan_ids_score[1][1] else clan_ids_score[1][0]
        delta = abs(clan_ids_score[0][1] - clan_ids_score[1][1]) // (members_count / 2)

        for current_participant in current_participants:
            if current_participant.clan_id == winner:
                current_participant.user.score += delta
                current_participant.user.d0 += delta

            else:
                current_participant.user.score = max(0, current_participant.user.score - delta)
                current_participant.user.d0 = current_participant.user.d0 - delta

        for passed_participant in (SaPassedClanWarParticipant(
            user_id=current_participant.user_id,
            passed_clan_war_id=passed_clan_war.id,
            clan_id=current_participant.clan_id,
            score=current_participant.score
        ) for current_participant in current_participants):
            create_object(passed_participant, session)

        delete_object(clan_war, session)

if __name__ == '__main__':
    check_clan_wars_time_span() # type: ignore