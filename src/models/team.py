import typing
from uuid import UUID
from sqlalchemy import ForeignKey
from src.api.v1.core.database import SQLBase, TableIdMixin
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Formations(str, Enum):
    form1 = "4-4-2"
    form2 = "4-3-3"
    form3 = "3-4-3"


if typing.TYPE_CHECKING:
    from src.models import Users


class Team(SQLBase, TableIdMixin):
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    members: Mapped[List["Users"]] = relationship("Users", back_populates="team")
    formation: Mapped[Formations] = mapped_column()
    score: Mapped[int] = mapped_column(default=0)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
