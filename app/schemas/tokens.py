from typing import Optional

from pydantic import BaseModel


class TokenInfoSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
