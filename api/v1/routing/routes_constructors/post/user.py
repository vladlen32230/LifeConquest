from fastapi import Depends, Body, HTTPException
from typing import Annotated
from models.other import Route
from models.sqlalchemy import SaUser
from models.pydantic.post import PdPostUser
from models.pydantic.returning import PdUser
from dependencies.db import get_session
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from queries.create import create_object
from other.convertations import convert_sqlalchemy_to_pydantic

def construct_post_user_v1() -> dict:
    entity_name = SaUser.get_table_name()

    async def _post_v1(
        user_info: Annotated[PdPostUser, Body()],
        session: Annotated[Session, Depends(get_session)]
    ):
        sa_user = SaUser(username=user_info.username, password=user_info.password)

        try:
            create_object(sa_user, session)
        except IntegrityError as e:
            if 'UniqueViolation' in e.args[0]:
                raise HTTPException(409)

            raise

        return convert_sqlalchemy_to_pydantic(sa_user, PdUser)

    _post_v1.__name__ = f'post_{entity_name}_v1'

    return Route(
        path=f'/{entity_name}',
        endpoint=_post_v1,
        status_code=201,
        response_model=PdUser,
        responses={409: {'description': 'Username is not unique'}},
        methods=['POST'],
        description=f'Post {entity_name}'
    ).__dict__