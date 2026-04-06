from typing import List, Optional

from sqlmodel import SQLModel


# ─── Base ──────────────────────────────────────────────────────────────────
class TeamBase(SQLModel):
    name: str
    headquarters: str


# ─── Request schemas ───────────────────────────────────────────────────────
class TeamCreate(TeamBase):
    pass


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None


# ─── Response schemas ──────────────────────────────────────────────────────
class TeamRead(TeamBase):
    id: int


class HeroBasicRead(SQLModel):
    """Schema reducido de Hero para evitar import circular en schemas."""
    id: int
    name: str
    secret_name: str
    age: Optional[int] = None


class TeamReadFull(TeamRead):
    """Team con heroes de la relación 1:N y de la N:M."""
    heroes: List[HeroBasicRead] = []       # 1:N  (hero.team_id = team.id)
    hero_links: List[HeroBasicRead] = []   # N:M  (via HeroTeamLink)
