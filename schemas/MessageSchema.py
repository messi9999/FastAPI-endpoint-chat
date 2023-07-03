from pydantic import BaseModel
from typing import Optional


class MessageSchema(BaseModel):
    id: Optional[int]
    content: str
    conversationId: Optional[int]

    class Config:
        orm_mode = True
