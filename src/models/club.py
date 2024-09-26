from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.api.v1.core.database import SQLBase, TableIdMixin
from src.models.player import Player


# Real clubs that Players belongs to
class Club(SQLBase, TableIdMixin):
    name: Mapped[str] = mapped_column()
    players: Mapped[List[Player] | None] = relationship("Player", back_populates="club")
