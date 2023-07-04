from pydantic import BaseModel
from typing import Optional


class ArticleSchema(BaseModel):
    id: Optional[int]
    title: str
    content: str
    url: str
    userId: Optional[int]

    class Config:
        orm_mode = True
