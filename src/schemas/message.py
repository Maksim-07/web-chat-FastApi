from pydantic import BaseModel


class MessageSchema(BaseModel):
    sender_id: int
    message: str


class CurrentMessageSchema(BaseModel):
    sender: str = ""
    content: str
