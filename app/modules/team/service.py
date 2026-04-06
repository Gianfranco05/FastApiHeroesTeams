from typing import List, Optional

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.modules.team.models import Team
from app.modules.team.schemas import TeamCreate, TeamUpdate


def create_team(session: Session, data: TeamCreate) -> Team:
    team = Team.model_validate(data)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def get_teams(session: Session) -> List[Team]:
    stmt = select(Team).options(
        selectinload(Team.heroes),
        selectinload(Team.hero_links),
    )
    return list(session.exec(stmt).all())


def get_team(session: Session, team_id: int) -> Optional[Team]:
    stmt = (
        select(Team)
        .where(Team.id == team_id)
        .options(
            selectinload(Team.heroes),
            selectinload(Team.hero_links),
        )
    )
    return session.exec(stmt).first()


def update_team(
    session: Session, team_id: int, data: TeamUpdate
) -> Optional[Team]:
    team = session.get(Team, team_id)
    if not team:
        return None
    team_data = data.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


def delete_team(session: Session, team_id: int) -> bool:
    team = session.get(Team, team_id)
    if not team:
        return False
    session.delete(team)
    session.commit()
    return True
