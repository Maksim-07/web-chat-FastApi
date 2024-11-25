from pydantic import BaseModel


class MessageSchema(BaseModel):
    sender_id: int
    message: str
