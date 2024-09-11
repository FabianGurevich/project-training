from src.models.user import Users
from src.api.v1.schemas.user import UserCreate
from src.api.v1.core.database import Session


class UserController:
    def __init__(self):
        self.user = Users()

    def create_user(user_info: UserCreate, session: Session) -> Users:
        user = Users.objects(session).create(user_info.model_dump())
        return user
