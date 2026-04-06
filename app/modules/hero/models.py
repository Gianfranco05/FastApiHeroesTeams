from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    # Solo para type hints: evita import circular en runtime
    from app.modules.team.models import Team
    from app.modules.weapon.models import Weapon


# ─────────────────────────────────────────────────────────────────────────────
# Tabla de enlace N:M  →  Hero ↔ Team
# La definimos en el módulo hero para que team/models.py la importe sin ciclos.
# ─────────────────────────────────────────────────────────────────────────────
class HeroTeamLink(SQLModel, table=True):
    """
    Relación N:M entre Hero y Team.
    PK compuesta (hero_id, team_id) evita duplicados automáticamente.
    ondelete='CASCADE' limpia los enlaces al borrar Hero o Team.
    """

    __tablename__ = "hero_team_link"

    hero_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("hero.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )
    team_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("team.id", ondelete="CASCADE"),
            primary_key=True,
            nullable=False,
        )
    )


# ─────────────────────────────────────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────────────────────────────────────
class Hero(SQLModel, table=True):
    """
    Entidad central con 3 tipos de relación:

    1:1  weapon   → Hero tiene una sola Weapon  (FK weapon_id en Hero)
    1:N  team     → Hero pertenece a un Team    (FK team_id   en Hero, lado N)
    N:M  teams    → Hero en múltiples Teams     (via HeroTeamLink)
    """

    __tablename__ = "hero"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    # ── Relación 1:1 con Weapon ───────────────────────────────────
    # La FK vive aquí: weapon_id → weapon.id
    weapon_id: Optional[int] = Field(default=None, foreign_key="weapon.id")
    weapon: Optional["Weapon"] = Relationship(back_populates="hero")

    # ── Relación 1:N con Team (FK en Hero, lado N) ────────────────
    # Varios Heroes pueden pertenecer al mismo Team
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional["Team"] = Relationship(back_populates="heroes")

    # ── Relación N:M con Team via HeroTeamLink ────────────────────
    # Un Hero puede estar en múltiples Teams y viceversa
    teams: List["Team"] = Relationship(
        back_populates="hero_links",
        link_model=HeroTeamLink,
    )
