from pydantic import BaseModel, Field
from typing import Optional, List
from Schemas.MessageSchema import MessageSchema


class ConversationSchema(BaseModel):
    id: Optional[int]
    userId: Optional[int]
    articleId: Optional[int]
    article: str
    messages: List[MessageSchema] = []

    class Config:
        orm_mode = True
