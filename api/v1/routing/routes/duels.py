from routing.routes_constructors.get import construct_get_by_id_route_v1
from routing.routes_constructors.extended_get import construct_extended_get_v1
from models.pydantic.extended import PdExtDuel
from models.pydantic.returning import PdDuel
from models.sqlalchemy import SaDuel, SaUser
from typing import Callable
from sqlalchemy import ColumnElement, or_

def _duels_get_checker_v1(current_user: SaUser, duel: SaDuel) -> bool:
    return current_user.id in (duel.user_1_id, duel.user_2_id)

def _duels_extended_checker_v1(current_user: SaUser) -> ColumnElement[bool]:
    return or_(SaDuel.user_1_id == current_user.id, SaDuel.user_2_id == current_user.id)

duels_get_by_id_v1 = construct_get_by_id_route_v1(SaDuel, PdDuel, _duels_get_checker_v1) # type: ignore
duels_extended_get_v1 = construct_extended_get_v1(SaDuel, PdExtDuel, PdDuel, _duels_extended_checker_v1)