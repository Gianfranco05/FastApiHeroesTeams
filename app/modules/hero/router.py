from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.modules.hero import service
from app.modules.hero.schemas import (
    HeroCreate,
    HeroRead,
    HeroReadFull,
    HeroTeamAssign,
    HeroUpdate,
    TeamBasicRead,
)

router = APIRouter(prefix="/heroes", tags=["heroes"])


# ─── CRUD ──────────────────────────────────────────────────────────────────
@router.post("/", response_model=HeroRead, status_code=201)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    return service.create_hero(session, hero)


@router.get("/", response_model=List[HeroReadFull])
def list_heroes(session: Session = Depends(get_session)):
    return service.get_heroes(session)


@router.get("/{hero_id}", response_model=HeroReadFull)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = service.get_hero(session, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}", response_model=HeroRead)
def update_hero(
    hero_id: int, data: HeroUpdate, session: Session = Depends(get_session)
):
    hero = service.update_hero(session, hero_id, data)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.delete("/{hero_id}", status_code=204)
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    if not service.delete_hero(session, hero_id):
        raise HTTPException(status_code=404, detail="Hero not found")


# ─── Relación N:M  Hero ↔ Team ─────────────────────────────────────────────
@router.post("/{hero_id}/teams", response_model=HeroReadFull)
def assign_to_team(
    hero_id: int,
    body: HeroTeamAssign,
    session: Session = Depends(get_session),
):
    """Agrega el Hero a un Team (N:M). Un Hero puede estar en múltiples Teams."""
    hero = service.add_hero_to_team(session, hero_id, body.team_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero or Team not found")
    return hero


@router.delete("/{hero_id}/teams/{team_id}", response_model=HeroReadFull)
def remove_from_team(
    hero_id: int,
    team_id: int,
    session: Session = Depends(get_session),
):
    """Elimina el Hero de un Team (elimina el registro en HeroTeamLink)."""
    hero = service.remove_hero_from_team(session, hero_id, team_id)
    if not hero:
        raise HTTPException(
            status_code=404, detail="Hero-Team relationship not found"
        )
    return hero


@router.get("/{hero_id}/teams", response_model=List[TeamBasicRead])
def get_hero_teams(hero_id: int, session: Session = Depends(get_session)):
    """Lista todos los Teams del Hero (N:M)."""
    return service.get_hero_teams(session, hero_id)
