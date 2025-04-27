from pydantic import BaseModel
from typing import Any
from other.convertations import convert_str_to_hashed_password

class PdPostBase(BaseModel):
    class Config:
        extra = 'forbid'

class PdPostUser(PdPostBase):
    username: str
    password: str

    def model_post_init(self, __context: Any) -> None:
        self.password = convert_str_to_hashed_password(self.password)

class PdPostClan(PdPostBase):
    clanname: str
    description: str

class PdPostClanRequest(PdPostBase):
    clan_id: int

class PdPostClanMembership(PdPostBase):
    user_id: int