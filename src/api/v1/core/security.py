from datetime import datetime, timedelta
from typing import Tuple
from fastapi.responses import Response
from src.api.v1.schemas import Token
from jose import jwt


class AuthManager:
    @staticmethod
    def create_token(user) -> Tuple[str, datetime]:
        claims = {
            "email": user.email,
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
