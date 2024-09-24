from uuid import UUID
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str
    position: str
    score: int


class PlayerCreate(PlayerBase):
    club_name: str


class Player(PlayerBase):
    club_id: UUID
