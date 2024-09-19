from fastapi import Request
from fastapi import Depends
from sqlalchemy import create_engine
from src.api.v1.core.security import AuthManager
from src.models.user import Users

from sqlalchemy.orm import (
    Session,
    sessionmaker,
)


engine = create_engine("postgresql://dev:dev@db:5432/dev", pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_user(request: Request, session: Session = Depends(get_session)) -> Users:
    manager = AuthManager()
    return manager(request=request, session=session)
