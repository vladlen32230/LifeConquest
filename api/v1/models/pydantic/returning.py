from pydantic import BaseModel
from datetime import datetime

class PdUserInfo(BaseModel):
    user: 'PdUser'

    clan: 'PdClan | None'
    clan_membership: 'PdClanMembership | None'

    division: 'PdDivision | None'
    division_membership: 'PdDivisionMembership | None'

    duel: 'PdDuel | None'

    clan_war: 'PdClanWar | None'
    clan_war_participant: 'PdClanWarParticipant | None'

    class Config:
        extra = 'forbid'
        from_attributes = True

class PdBase(BaseModel):
    id: int

    class Config:
        extra = 'forbid'
        from_attributes = True

class PdUser(PdBase):
    username: str
    score: int
    created_at: datetime
    participate_division: bool
    occupied: bool

    d0: int
    d1: int
    d2: int
    d3: int
    d4: int
    d5: int
    d6: int

class PdClan(PdBase):
    clanname: str
    owner_membership_id: int | None
    created_at: datetime
    description: str
    recruiting: bool

class PdClanRequest(PdBase):
    user_id: int
    clan_id: int
    created_at: datetime

class PdClanMembership(PdBase):
    user_id: int
    clan_id: int
    joined_at: datetime

class PdDivision(PdBase):
    started_at: datetime

class PdDivisionMembership(PdBase):
    user_id: int | None
    division_id: int
    score: int

class PdPassedDivision(PdBase):
    ended_at: datetime

class PdPassedDivisionMembership(PdBase):
    user_id: int | None
    passed_division_id: int
    score: int

class PdDuel(PdBase):
    user_1_id: int
    user_1_score: int
    user_2_id: int
    user_2_score: int
    started_at: datetime

class PdPassedDuel(PdBase):
    user_1_id: int | None
    user_1_score: int
    user_2_id: int | None
    user_2_score: int
    ended_at: datetime

class PdDuelInvite(PdBase):
    user_id: int
    created_at: datetime

class PdClanWar(PdBase):
    clan_1_id: int
    clan_2_id: int
    started_at: datetime

class PdClanWarParticipant(PdBase):
    user_membership_id: int | None
    user_id: int | None
    clan_war_id: int
    clan_id: int
    score: int

class PdPassedClanWar(PdBase):
    clan_1_id: int | None
    clan_2_id: int | None
    ended_at: datetime

class PdPassedClanWarParticipant(PdBase):
    user_id: int | None
    passed_clan_war_id: int
    clan_id: int | None
    score: int

class PdClanWarInvite(PdBase):
    clan_id: int
    created_at: datetime

class PdClanWarPostResponseModel(BaseModel):
    clan_war_started: bool
    model: PdClanWar | PdClanWarInvite

class PdDuelPostResponseModel(BaseModel):
    duel_started: bool
    model: PdDuel | PdDuelInvite