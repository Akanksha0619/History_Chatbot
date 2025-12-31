from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
   

class UserUpdate(BaseModel):
    name: Optional[str] = None
