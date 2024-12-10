from datetime import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    sub: str
    name: str
    exp: datetime
