from pydantic import BaseModel, Field
from datetime import datetime
from sqlalchemy import asc, desc
from fastapi import HTTPException
from models.sqlalchemy import (
    SaUser, SaBase, 
    SaClan, SaClanRequest, 
    SaClanMembership, SaDivision, 
    SaDivisionMembership, SaClanWar,
    SaClanWarInvite, SaClanWarParticipant,
    SaPassedClanWar, SaPassedClanWarParticipant,
    SaPassedDivision, SaPassedDivisionMembership,
    SaPassedDuel, SaDuel, SaDuelInvite
)

class PdExtBase(BaseModel):
    class Config:
        extra = 'forbid'

    _sa_entity: type[SaBase]
    
    id: list[int] = Field(default_factory=list)
    sort_by: list[str] = Field(default_factory=list)
    offset: int | None = Field(None, ge=0)
    limit: int | None = Field(None, ge=0)

    @property
    def where_order_clause(self) -> tuple[list, list]:
        all_fields = self.__dict__

        sort_fields = all_fields['sort_by']
        attributes = {
            key: val for key, val in all_fields.items() 
            if key not in ('sort_by', 'offset', 'limit')
        }

        order = []
        for sort_field in sort_fields:
            field_name = sort_field[1:]
            sign = sort_field[0]

            if field_name not in attributes or sign not in ('+', '-'):
                raise HTTPException(422)

            attr = getattr(self._sa_entity, field_name)
            order.append(asc(attr) if sign == '+' else desc(attr))

        where = []
        for name, values in attributes.items():
            if len(values) > 0:
                where.append(getattr(self._sa_entity, name).in_(values))

        return (where, order)

class PdExtUser(PdExtBase):
    _sa_entity = SaUser

    username: list[str] = Field(default_factory=list)
    score: list[int] = Field(default_factory=list)
    created_at: list[datetime] = Field(default_factory=list)
    participate_division: list[bool] = Field(default_factory=list)

    occupied: list[bool] = Field(default_factory=list)

    d0: list[int] = Field(default_factory=list)
    d1: list[int] = Field(default_factory=list)
    d2: list[int] = Field(default_factory=list)
    d3: list[int] = Field(default_factory=list)
    d4: list[int] = Field(default_factory=list)
    d5: list[int] = Field(default_factory=list)
    d6: list[int] = Field(default_factory=list)

class PdExtClan(PdExtBase):
    _sa_entity = SaClan

    clanname: list[str] = Field(default_factory=list)
    owner_membership_id: list[int] = Field(default_factory=list)
    created_at: list[datetime] = Field(default_factory=list)
    description: list[str] = Field(default_factory=list)
    recruiting: list[bool] = Field(default_factory=list)

class PdExtClanRequest(PdExtBase):
    _sa_entity = SaClanRequest

    user_id: list[int] = Field(default_factory=list)
    clan_id: list[int] = Field(default_factory=list)
    created_at: list[datetime] = Field(default_factory=list)

class PdExtClanMembership(PdExtBase):
    _sa_entity = SaClanMembership

    user_id: list[int] = Field(default_factory=list)
    clan_id: list[int] = Field(default_factory=list)
    joined_at: list[datetime] = Field(default_factory=list)

class PdExtDivision(PdExtBase):
    _sa_entity = SaDivision

    started_at: list[datetime] = Field(default_factory=list)

class PdExtDivisionMembership(PdExtBase):
    _sa_entity = SaDivisionMembership

    user_id: list[int | None] = Field(default_factory=list)
    division_id: list[int] = Field(default_factory=list)
    score: list[int] = Field(default_factory=list)

class PdExtPassedDivision(PdExtBase):
    _sa_entity = SaPassedDivision

    ended_at: list[datetime] = Field(default_factory=list)

class PdExtPassedDivisionMembership(PdExtBase):
    _sa_entity = SaPassedDivisionMembership

    user_id: list[int | None] = Field(default_factory=list)
    passed_division_id: list[int] = Field(default_factory=list)
    score: list[int] = Field(default_factory=list)

class PdExtDuel(PdExtBase):
    _sa_entity = SaDuel

    user_1_id: list[int] = Field(default_factory=list)
    user_1_score: list[int] = Field(default_factory=list)
    user_2_id: list[int] = Field(default_factory=list)
    user_2_score: list[int] = Field(default_factory=list)
    started_at: list[datetime] = Field(default_factory=list)

class PdExtPassedDuel(PdExtBase):
    _sa_entity = SaPassedDuel

    user_1_id: list[int | None] = Field(default_factory=list)
    user_1_score: list[int] = Field(default_factory=list)
    user_2_id: list[int | None] = Field(default_factory=list)
    user_2_score: list[int] = Field(default_factory=list)
    ended_at: list[datetime] = Field(default_factory=list)

class PdExtDuelInvite(PdExtBase):
    _sa_entity = SaDuelInvite

    user_id: list[int] = Field(default_factory=list)
    created_at: list[int] = Field(default_factory=list)

class PdExtClanWar(PdExtBase):
    _sa_entity = SaClanWar

    clan_1_id: list[int] = Field(default_factory=list)
    clan_2_id: list[int] = Field(default_factory=list)
    started_at: list[datetime] = Field(default_factory=list)

class PdExtClanWarParticipant(PdExtBase):
    _sa_entity = SaClanWarParticipant

    user_membership_id: list[int | None] = Field(default_factory=list)
    user_id: list[int | None] = Field(default_factory=list)
    clan_war_id: list[int] = Field(default_factory=list)
    clan_id: list[int] = Field(default_factory=list)
    score: list[int] = Field(default_factory=list)

class PdExtPassedClanWar(PdExtBase):
    _sa_entity = SaPassedClanWar

    clan_1_id: list[int | None] = Field(default_factory=list)
    clan_2_id: list[int | None] = Field(default_factory=list)
    ended_at: list[datetime] = Field(default_factory=list)

class PdExtPassedClanWarParticipant(PdExtBase):
    _sa_entity = SaPassedClanWarParticipant

    user_id: list[int | None] = Field(default_factory=list)
    passed_clan_war_id: list[int] = Field(default_factory=list)
    clan_id: list[int | None] = Field(default_factory=list)
    score: list[int] = Field(default_factory=list)

class PdExtClanWarInvite(PdExtBase):
    _sa_entity = SaClanWarInvite

    clan_id: list[int] = Field(default_factory=list)
    created_at: list[datetime] = Field(default_factory=list)