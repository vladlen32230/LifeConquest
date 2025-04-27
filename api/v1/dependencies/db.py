from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from other.constants import POSTGRESQL_URL
from typing import Generator

engine = create_engine(
    POSTGRESQL_URL, 
    #echo='debug'
)

def get_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close()