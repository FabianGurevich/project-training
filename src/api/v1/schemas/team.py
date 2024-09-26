from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from src.models.team import Formations
from pydantic import ConfigDict


class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    formation: Formations


class AddRemovePlayer(BaseModel):
    team_id: UUID
    player_id: UUID


class Team(TeamCreate):
    score: int = 0
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class TeamInfo(Team):
    players: list[str]
    model_config = ConfigDict(from_attributes=True)


class TeamUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    formation: Formations | None = None
