from sqlalchemy.orm import Mapped, mapped_column
from src.api.v1.core.database import SQLBase, TableIdMixin


class Users(SQLBase, TableIdMixin):
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    def __str__(self) -> str:
        return self.name
