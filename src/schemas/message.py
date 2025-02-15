from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    sender_id: int
    message: str


class CurrentMessageSchema(BaseModel):
    login: str = Field(default="")
    message: str
