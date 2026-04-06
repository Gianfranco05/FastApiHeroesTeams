from typing import List, Optional

from sqlmodel import SQLModel

from app.modules.weapon.schemas import WeaponRead


# ─── Base ──────────────────────────────────────────────────────────────────
class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None


# ─── Request schemas ───────────────────────────────────────────────────────
class HeroCreate(HeroBase):
    team_id: Optional[int] = None      # 1:N  – asignar equipo principal
    weapon_id: Optional[int] = None    # 1:1  – asignar arma


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None
    team_id: Optional[int] = None
    weapon_id: Optional[int] = None


# ─── Response schemas ──────────────────────────────────────────────────────
class HeroRead(HeroBase):
    id: int
    team_id: Optional[int] = None
    weapon_id: Optional[int] = None


class TeamBasicRead(SQLModel):
    """Schema reducido de Team para evitar import circular en schemas."""
    id: int
    name: str
    headquarters: str


class HeroReadFull(HeroRead):
    """Hero con todas sus relaciones anidadas."""
    weapon: Optional[WeaponRead] = None
    team: Optional[TeamBasicRead] = None
    teams: List[TeamBasicRead] = []


# ─── Operaciones N:M ──────────────────────────────────────────────────────
class HeroTeamAssign(SQLModel):
    team_id: int
