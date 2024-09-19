from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_at: datetime


class TokenPayload(BaseModel):
    user_id: str
