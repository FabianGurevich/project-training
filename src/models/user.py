import typing
from sqlalchemy.orm import Mapped, mapped_column
from src.api.v1.core.database import SQLBase, TableIdMixin
from sqlalchemy.orm import relationship


if typing.TYPE_CHECKING:
    from src.models import Team


class Users(SQLBase, TableIdMixin):
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    team: Mapped["Team"] = relationship("Team", back_populates="members")
