from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    name: str
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
