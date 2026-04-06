from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.modules.hero.models import Hero, HeroTeamLink
from app.modules.hero.schemas import HeroCreate, HeroUpdate
from app.modules.team.models import Team


# ─── CRUD básico ──────────────────────────────────────────────────────────
def create_hero(session: Session, data: HeroCreate) -> Hero:
    hero = Hero.model_validate(data)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def get_heroes(session: Session) -> List[Hero]:
    stmt = select(Hero).options(
        selectinload(Hero.weapon),
        selectinload(Hero.team),
        selectinload(Hero.teams),
    )
    return list(session.exec(stmt).all())


def get_hero(session: Session, hero_id: int) -> Optional[Hero]:
    stmt = (
        select(Hero)
        .where(Hero.id == hero_id)
        .options(
            selectinload(Hero.weapon),
            selectinload(Hero.team),
            selectinload(Hero.teams),
        )
    )
    return session.exec(stmt).first()


def update_hero(
    session: Session, hero_id: int, data: HeroUpdate
) -> Optional[Hero]:
    hero = session.get(Hero, hero_id)
    if not hero:
        return None
    hero_data = data.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero, key, value)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def delete_hero(session: Session, hero_id: int) -> bool:
    hero = session.get(Hero, hero_id)
    if not hero:
        return False
    session.delete(hero)
    session.commit()
    return True


# ─── Operaciones N:M  Hero ↔ Team ─────────────────────────────────────────
def add_hero_to_team(
    session: Session, hero_id: int, team_id: int
) -> Optional[Hero]:
    """Agrega un Hero a un Team via la tabla HeroTeamLink (N:M)."""
    hero = session.get(Hero, hero_id)
    team = session.get(Team, team_id)
    if not hero or not team:
        return None

    # Verificar si el enlace ya existe para no duplicar
    existing = session.exec(
        select(HeroTeamLink).where(
            HeroTeamLink.hero_id == hero_id,
            HeroTeamLink.team_id == team_id,
        )
    ).first()

    if not existing:
        link = HeroTeamLink(hero_id=hero_id, team_id=team_id)
        session.add(link)
        session.commit()

    # Recargar con relaciones
    return get_hero(session, hero_id)


def remove_hero_from_team(
    session: Session, hero_id: int, team_id: int
) -> Optional[Hero]:
    """Elimina el enlace N:M entre un Hero y un Team."""
    link = session.exec(
        select(HeroTeamLink).where(
            HeroTeamLink.hero_id == hero_id,
            HeroTeamLink.team_id == team_id,
        )
    ).first()

    if not link:
        return None

    session.delete(link)
    session.commit()
    return get_hero(session, hero_id)


def get_hero_teams(session: Session, hero_id: int) -> List[Team]:
    """Retorna todos los Teams a los que pertenece un Hero (N:M)."""
    hero = get_hero(session, hero_id)
    if not hero:
        return []
    return hero.teams
