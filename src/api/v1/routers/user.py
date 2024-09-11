from fastapi import APIRouter
from fastapi import Depends

from src.api.v1.schemas.user import User, UserCreate
from src.api.v1.core.database import get_session, Session
from src.controllers.user import UserController

router = APIRouter()


@router.post("", status_code=201)
def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session),
) -> User:
    user = UserController.create_user(user_info=user_data, session=session)
    return user
