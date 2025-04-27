from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDuel
from models.pydantic.returning import PdPassedDuel
from models.sqlalchemy import SaPassedDuel, SaUser
from sqlalchemy import or_, ColumnElement

def _passed_duels_get_checker_v1(current_user: SaUser, passed_duel: SaPassedDuel) -> bool:
    return current_user.id in (passed_duel.user_1_id, passed_duel.user_2_id)

def _passed_duels_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    return or_(SaPassedDuel.user_1_id == current_user.id, SaPassedDuel.user_2_id == current_user.id)

passed_duels_get_by_id_v1 = construct_get_by_id_route_v1(
    SaPassedDuel, 
    PdPassedDuel, 
    _passed_duels_get_checker_v1 # type: ignore
)

passed_duels_extended_get_v1 = construct_extended_get_v1(
    SaPassedDuel,
    PdExtDuel,
    PdPassedDuel,
    _passed_duels_extended_checker_v1
)