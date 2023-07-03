from pydantic import BaseModel, Field
from typing import Optional, List


class ArticleSchema(BaseModel):
    id: Optional[int]
    title: str
    content: str
    url: str
    userId: Optional[int]

    class Config:
        orm_mode = True
