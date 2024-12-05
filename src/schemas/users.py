from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    login: str
    password: str


class UserRegisterSchema(UserBaseSchema):
    pass


class UserAuthSchema(UserBaseSchema):
    pass


class UserIdSchema(BaseModel):
    id: int


class UserLoginSchema(BaseModel):
    login: str
