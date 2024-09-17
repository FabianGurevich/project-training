from fastapi import HTTPException
from src.models.user import Users
from src.api.v1.schemas import UserCreate, UserLogin
from src.api.v1.core.database import Session


class UserController:
    def __init__(self):
        self.user = Users()

    def create_user(user_info: UserCreate, session: Session) -> Users:
        email_exists = Users.objects(session).get(Users.email == user_info.email)
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already exists")
        user = Users.objects(session).create(user_info.model_dump())
        return user

    def login_user(user_info: UserLogin, session: Session) -> Users:
        user = Users.objects(session).get(Users.email == user_info.email)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        if user.password != user_info.password:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return user
