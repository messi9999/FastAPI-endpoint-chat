from pydantic import BaseModel
from typing import Optional


class CreateConversatiionSchema(BaseModel):
    user_id: Optional[int]
    url: str

    class Config:
        orm_mode = True
