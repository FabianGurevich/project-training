from fastapi import APIRouter, Response
from fastapi import Depends

from src.api.v1.core.dependencies import get_session
from src.api.v1.schemas.user import UserCreate, UserBase, UserLogin
from src.api.v1.schemas.token import Token
from src.api.v1.core.database import Session
from src.controllers.user import UserController
from src.api.v1.core.security import AuthManager

router = APIRouter()


@router.post("", status_code=201)
def signup(
    user_data: UserCreate,
    session: Session = Depends(get_session),
) -> UserBase:
    user = UserController.create_user(user_info=user_data, session=session)
    return user


@router.post("/login", status_code=200)
def login(
    response: Response,
    user_data: UserLogin,
    session: Session = Depends(get_session),
) -> Token:
    user = UserController.login_user(user_info=user_data, session=session)
    return AuthManager.process__login(user=user, response=response)
