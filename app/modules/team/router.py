from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.modules.team import service
from app.modules.team.schemas import TeamCreate, TeamRead, TeamReadFull, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamRead, status_code=201)
def create_team(team: TeamCreate, session: Session = Depends(get_session)):
    return service.create_team(session, team)


@router.get("/", response_model=List[TeamReadFull])
def list_teams(session: Session = Depends(get_session)):
    return service.get_teams(session)


@router.get("/{team_id}", response_model=TeamReadFull)
def get_team(team_id: int, session: Session = Depends(get_session)):
    team = service.get_team(session, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int, data: TeamUpdate, session: Session = Depends(get_session)
):
    team = service.update_team(session, team_id, data)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, session: Session = Depends(get_session)):
    if not service.delete_team(session, team_id):
        raise HTTPException(status_code=404, detail="Team not found")
