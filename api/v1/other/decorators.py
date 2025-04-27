from dependencies.db import get_session
from sqlalchemy.orm import Session
from typing import Callable

def script(func: Callable[[Session], None]):
    def wrapper():
        session_generator = get_session()

        session = next(session_generator)

        func(session)

        try:
            next(session_generator)
        except StopIteration:
            pass

    return wrapper