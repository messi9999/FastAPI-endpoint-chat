from pydantic import BaseModel
from typing import Optional


class ChatSchema(BaseModel):
    conversation_id: Optional[int]
    message: str
