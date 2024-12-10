from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    login: str
    password: str


class UserRegisterFormSchema(BaseModel):
    username: str
    password: str


class CurrentUserSchema(BaseModel):
    id: int
    login: str
