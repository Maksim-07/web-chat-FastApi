from datetime import datetime

from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    id: int
    login: str
    created_at: datetime
    updated_at: datetime | None = Field(default=None)


class UserRegisterFormSchema(BaseModel):
    username: str
    password: str


class CurrentUserSchema(BaseModel):
    id: int
    login: str
