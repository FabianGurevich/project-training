from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
