from enum import Enum
from typing import List
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.api.v1.core.database import SQLBase, TableIdMixin
from sqlalchemy import ForeignKey
from src.models.team import Team
from src.models.team_player import team_player_table


class Positions(str, Enum):
    GOALKEEPER = "Goalkeeper"
    DEFENDER = "Defender"
    MIDFIELDER = "Midfielder"
    FORWARD = "Forward"


class Player(SQLBase, TableIdMixin):
    name: Mapped[str] = mapped_column()
    club_id: Mapped[UUID] = mapped_column(ForeignKey("club.id"))
    club: Mapped["Club"] = relationship("Club", back_populates="players")
    position: Mapped[Positions] = mapped_column()
    score: Mapped[int] = mapped_column(default=0)
    teams: Mapped[List[Team] | None] = relationship(
        secondary=team_player_table, back_populates="players"
    )


# Players tienen un solo club pero un club tiene muchos players
