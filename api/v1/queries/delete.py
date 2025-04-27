from models.sqlalchemy import SaBase
from sqlalchemy import delete
from sqlalchemy.orm import Session

def delete_object(sa_instance: SaBase, session: Session) -> None:
    session.delete(sa_instance)
    session.flush()

def delete_object_by_id(id: int, sa_entity: type[SaBase], session: Session) -> None:
    stmt = delete(sa_entity).where(sa_entity.id == id)
    session.execute(stmt)
    session.flush()

def delete_objects_by_filters(where_clause: list, sa_entity: type[SaBase], session: Session) -> None:
    stmt = delete(sa_entity).where(*where_clause)
    session.execute(stmt)
    session.flush()