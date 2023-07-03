from pydantic import BaseModel
from typing import Optional, List


class ChatSchema(BaseModel):
    conversation_id: Optional[int]
    message: str
