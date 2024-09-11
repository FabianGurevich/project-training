from sqlalchemy.orm import Mapped, mapped_column
from src.api.v1.core.database import SQLBase


class Users(SQLBase):
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
