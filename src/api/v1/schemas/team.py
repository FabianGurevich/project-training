from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from src.models.team import Formations
from pydantic import ConfigDict


class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None
    formation: Formations


class Team(TeamCreate):
    score: int = 0
    id: UUID
    model_config = ConfigDict(from_attributes=True)
