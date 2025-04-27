from models.sqlalchemy import SaBase
from sqlalchemy import update, ScalarResult
from sqlalchemy.orm import Session
from typing import Any

def patch_object(sa_instance: SaBase, attributes: dict[str, Any], session: Session) -> SaBase:
    for name, value in attributes.items():
        setattr(sa_instance, name, value)

    session.flush()
    return sa_instance

def update_objects_values(sa_entity: type[SaBase], where_clause: list, values: dict, session: Session) -> None:
    stmt = update(sa_entity).where(*where_clause).values(values)
    session.execute(stmt)
    session.flush()