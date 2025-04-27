from sqlalchemy import String, func, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Relationship
from datetime import datetime
from typing import Optional

class SaBase(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_table_name(cls) -> str:
        return cls.__tablename__

class SaUser(SaBase):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(64))
    score: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    daily_task: Mapped[bool] = mapped_column(default=False)
    participate_division: Mapped[bool] = mapped_column(default=False)

    occupied: Mapped[bool] = mapped_column(default=False)

    d0: Mapped[int] = mapped_column(default=0)
    d1: Mapped[int] = mapped_column(default=0)
    d2: Mapped[int] = mapped_column(default=0)
    d3: Mapped[int] = mapped_column(default=0)
    d4: Mapped[int] = mapped_column(default=0)
    d5: Mapped[int] = mapped_column(default=0)
    d6: Mapped[int] = mapped_column(default=0)

    clan_membership: Mapped['SaClanMembership'] = Relationship(
        'SaClanMembership', 
        back_populates='user',
        cascade='all, delete'
    )

class SaClan(SaBase):
    __tablename__ = 'clans'

    clanname: Mapped[str] = mapped_column(String(32), unique=True)
    owner_membership_id: Mapped[Optional[int]] = mapped_column(ForeignKey('clan_memberships.id', ondelete='CASCADE'), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    description: Mapped[str] = mapped_column(default='')
    recruiting: Mapped[bool] = mapped_column(default=False)

    members: Mapped[list['SaClanMembership']] = Relationship(
        'SaClanMembership', 
        back_populates='clan', 
        primaryjoin='SaClan.id == SaClanMembership.clan_id',
        cascade='all, delete'
    )

class SaClanRequest(SaBase):
    __tablename__ = 'clan_requests'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    clan_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    clan: Mapped[SaClan] = Relationship('SaClan')

    __table_args__ = (
        UniqueConstraint('user_id', 'clan_id', name='user_clan_unique'),
    )

class SaClanMembership(SaBase):
    __tablename__ = 'clan_memberships'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    clan_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'))
    joined_at: Mapped[datetime] = mapped_column(default=func.now())

    clan: Mapped[SaClan] = Relationship('SaClan', back_populates='members', primaryjoin='SaClan.id == SaClanMembership.clan_id')
    user: Mapped[SaUser] = Relationship('SaUser', back_populates='clan_membership')

class SaDivision(SaBase):
    __tablename__ = 'divisions'

    started_at: Mapped[datetime] = mapped_column(default=func.now())

    memberships: Mapped[list['SaDivisionMembership']] = Relationship(
        'SaDivisionMembership', 
        back_populates='division',
        cascade='all, delete'
    )

class SaDivisionMembership(SaBase):
    __tablename__ = 'division_memberships'

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), unique=True)
    division_id: Mapped[int] = mapped_column(ForeignKey('divisions.id', ondelete='CASCADE'))
    score: Mapped[int] = mapped_column(SmallInteger(), default=0)

    division: Mapped[SaDivision] = Relationship(
        'SaDivision', 
        back_populates='memberships'
    )

class SaPassedDivision(SaBase):
    __tablename__ = 'passed_divisions'

    ended_at: Mapped[datetime] = mapped_column(default=func.now())

    memberships: Mapped[list['SaPassedDivisionMembership']] = Relationship(
        'SaPassedDivisionMembership', 
        back_populates='passed_division',
        cascade='all, delete'
    )

class SaPassedDivisionMembership(SaBase):
    __tablename__ = 'passed_division_memberships'

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    passed_division_id: Mapped[int] = mapped_column(ForeignKey('passed_divisions.id'))
    score: Mapped[int] = mapped_column(SmallInteger())

    passed_division: Mapped[SaPassedDivision] = Relationship(
        'SaPassedDivision', 
        back_populates='memberships'
    )

class SaDuel(SaBase):
    __tablename__ = 'duels'

    user_1_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    user_1_score: Mapped[int] = mapped_column(SmallInteger(), default=0)
    user_2_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    user_2_score: Mapped[int] = mapped_column(SmallInteger(), default=0)
    started_at: Mapped[datetime] = mapped_column(default=func.now())

class SaPassedDuel(SaBase):
    __tablename__ = 'passed_duels'

    user_1_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    user_1_score: Mapped[int] = mapped_column(SmallInteger())
    user_2_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    user_2_score: Mapped[int] = mapped_column(SmallInteger())
    ended_at: Mapped[datetime] = mapped_column(default=func.now())

class SaDuelInvite(SaBase):
    __tablename__ = 'duel_invites'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

class SaClanWar(SaBase):
    __tablename__ = 'clan_wars'

    clan_1_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'), unique=True)
    clan_2_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'), unique=True)
    started_at: Mapped[datetime] = mapped_column(default=func.now())

    clan_1: Mapped[SaClan] = Relationship('SaClan', foreign_keys=[clan_1_id])
    clan_2: Mapped[SaClan] = Relationship('SaClan', foreign_keys=[clan_2_id])
    participants: Mapped[list['SaClanWarParticipant']] = Relationship(
        'SaClanWarParticipant', 
        back_populates='clan_war', 
        cascade='all, delete'
    )

class SaClanWarParticipant(SaBase):
    __tablename__ = 'clan_war_participants'

    user_membership_id: Mapped[Optional[int]] = mapped_column(ForeignKey('clan_memberships.id', ondelete='SET NULL'), unique=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), unique=True)
    clan_war_id: Mapped[int] = mapped_column(ForeignKey('clan_wars.id', ondelete='CASCADE'))
    clan_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'))
    score: Mapped[int] = mapped_column(SmallInteger(), default=0)

    clan_war: Mapped[SaClanWar] = Relationship('SaClanWar', back_populates='participants')
    clan: Mapped[SaClan] = Relationship('SaClan')
    user: Mapped[SaUser] = Relationship('SaUser')

class SaPassedClanWar(SaBase):
    __tablename__ = 'passed_clan_wars'

    clan_1_id: Mapped[Optional[int]] = mapped_column(ForeignKey('clans.id', ondelete='SET NULL'))
    clan_2_id: Mapped[Optional[int]] = mapped_column(ForeignKey('clans.id', ondelete='SET NULL'))
    ended_at: Mapped[datetime] = mapped_column(default=func.now())

    clan_1: Mapped[SaClan] = Relationship('SaClan', foreign_keys=[clan_1_id])
    clan_2: Mapped[SaClan] = Relationship('SaClan', foreign_keys=[clan_2_id])

class SaPassedClanWarParticipant(SaBase):
    __tablename__ = 'passed_clan_war_participants'

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))
    passed_clan_war_id: Mapped[int] = mapped_column(ForeignKey('passed_clan_wars.id', ondelete='CASCADE'))
    clan_id: Mapped[Optional[int]] = mapped_column(ForeignKey('clans.id', ondelete='SET NULL'))
    score: Mapped[int] = mapped_column(SmallInteger())

    passed_clan_war: Mapped[SaPassedClanWar] = Relationship('SaPassedClanWar')
    clan: Mapped[SaClan] = Relationship('SaClan')

class SaClanWarInvite(SaBase):
    __tablename__ = 'clan_war_invite'

    clan_id: Mapped[int] = mapped_column(ForeignKey('clans.id', ondelete='CASCADE'), unique=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    clan: Mapped[SaClan] = Relationship('SaClan')