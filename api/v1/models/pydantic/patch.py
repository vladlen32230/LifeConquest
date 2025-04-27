from pydantic import BaseModel
from typing import Any
from other.convertations import convert_str_to_hashed_password

class PdPatchBase(BaseModel):
    class Config:
        extra = 'forbid'

class PdPatchUser(PdPatchBase):
    username: str | None = None
    password: str | None = None
    participate_division: bool | None = None

    def model_post_init(self, __context: Any) -> None:
        if self.password is not None:
            self.password = convert_str_to_hashed_password(self.password)

class PdPatchClan(PdPatchBase):
    clanname: str | None = None
    recruiting: bool | None = None
    description: str | None = None