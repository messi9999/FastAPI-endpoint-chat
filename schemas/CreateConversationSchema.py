from pydantic import BaseModel, Field
from typing import Optional, List
from Schemas.MessageSchema import MessageSchema


class CreateConversatiionSchema(BaseModel):
    user_id: Optional[int]
    url: str

    class Config:
        orm_mode = True
