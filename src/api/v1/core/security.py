from datetime import datetime, timedelta
from fastapi.responses import Response
from src.api.v1.schemas import Token
from jose import jwt


class AuthManager:
    @staticmethod
    def create_token(user):
        claims = {
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return jwt.encode(
            claims=claims,
            key="super_secret_jeje",
            algorithm="HS256",
        )

    def set__cookie(response: Response, key, value):
        response.set_cookie(key=key, value=value, httponly=True)

    @classmethod
    def process__login(self, user, response) -> Token:
        token = self.create_token(user)
        self.set__cookie(response, key="token", value=token)
        return Token(access_token=token)
