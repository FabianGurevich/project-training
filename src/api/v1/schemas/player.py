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


class PlayerUpdate(BaseModel):
    name: str | None = None
    position: str | None = None
    score: int | None = None
    club_name: str | None = None
