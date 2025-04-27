from sqlalchemy import select, ScalarResult, Row, Select, Result
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from models.sqlalchemy import SaBase
from typing import Any, Sequence

def read_object_by_id(id: int, sa_entity: type[SaBase], session: Session) -> SaBase | None:
    stmt = select(sa_entity).where(sa_entity.id == id)
    instance = session.execute(stmt).scalar_one_or_none()
    return instance

def read_objects_by_filters(
    where_clause: list, 
    order: list, 
    sa_entity: type[SaBase], 
    offset: int | None, 
    limit: int | None, 
    session: Session,
) -> ScalarResult[SaBase]:
    stmt = select(sa_entity).where(*where_clause).order_by(*order)

    if offset is not None:
        stmt = stmt.offset(offset)

    if limit is not None:
        stmt = stmt.limit(limit)

    instances = session.execute(stmt).scalars()
    return instances

def read_object_by_filters(
    where_clause: list, 
    sa_entity: type[SaBase], 
    session: Session, 
    order_by: list | None = None
) -> SaBase | None:
    stmt = select(sa_entity).where(*where_clause)

    if order_by is not None:
        stmt = stmt.order_by(*order_by)
        
    instance = session.execute(stmt).scalar_one_or_none()
    return instance

def exist_objects_by_fiters(where_clause: list, sa_entity: type[SaBase], session: Session) -> bool:
    stmt = exists(sa_entity).where(*where_clause)
    exist = session.query(stmt).scalar()
    return exist

def read_custom_stmt(stmt: Select, session: Session) -> Result:
    return session.execute(stmt)