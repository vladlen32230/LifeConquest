from models.sqlalchemy import SaBase
from sqlalchemy.orm import Session

def create_object(instance: SaBase, session: Session) -> SaBase:
    session.add(instance)
    session.flush()
    return instance