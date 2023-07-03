from pydantic import BaseModel
from typing import Optional, List
from Schemas.ConversationSchema import ConversationSchema
from Schemas.ArticleSchema import ArticleSchema


class UserSchema(BaseModel):
    id: Optional[int]
    username: str
    conversations: List[ConversationSchema] = []
    articles: List[ArticleSchema] = []

    class Config:
        orm_mode = True
