from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    password: str


class UserRegister(UserBase):
    pass


class UserAuth(UserBase):
    pass
