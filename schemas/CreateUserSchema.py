from pydantic import BaseModel, Field


class CreateUserSchema(BaseModel):
    name: str = Field(..., description="User Name")
