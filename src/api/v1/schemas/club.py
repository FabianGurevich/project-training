from pydantic import BaseModel


class CreateClub(BaseModel):
    name: str
