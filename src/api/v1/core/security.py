from datetime import datetime, timedelta
from typing import Tuple
from fastapi import HTTPException, Request
from fastapi.responses import Response
from pydantic import ValidationError
from src.api.v1.schemas import Token
from jose import JWTError, jwt
from src.api.v1.core.database import Session

from src.api.v1.schemas.token import TokenPayload
from src.models.user import Users


class AuthManager:

    def __call__(self, request: Request, session: Session) -> Users:
        token = self._get_token(request)
        return self.get_user_from_token(token, session)

    @staticmethod
    def create_token(user) -> Tuple[str, datetime]:
        claims = {
            "user_id": str(user.id),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return [
            jwt.encode(
                claims=claims,
                key="super_secret_jeje",
                algorithm="HS256",
            ),
            claims["exp"],
        ]

    def set__cookie(response: Response, key, value):
        response.set_cookie(key=key, value=value, httponly=True)

    @classmethod
    def process__login(self, user, response) -> Token:
        token, exp = self.create_token(user)
        self.set__cookie(response, key="token", value=token)
        return Token(access_token=token, expires_at=exp)

    def get_user_from_token(self, token: str, session: Session) -> Users:
        try:
            payload = jwt.decode(
                token=token, key="super_secret_jeje", algorithms="HS256"
            )
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            )
        user = Users.objects(session).get(Users.id == token_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def _get_token(self, request: Request) -> str:
        token = None
        token = self._get_token_from_cookie(request)
        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return token

    def _get_token_from_cookie(self, request: Request) -> str | None:
        token = request.cookies.get("token")
        return token
