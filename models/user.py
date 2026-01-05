from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
