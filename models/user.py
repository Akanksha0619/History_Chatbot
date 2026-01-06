from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    password: str
    email: EmailStr
    phone: int
    role: Optional[str] = "user"


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    password: Optional[str] = None
    phone: Optional[int] = None
    role: Optional[str] = None

    
    class Config:
        json_schema_extra = {"example": {

            "name":"user",
            "password":"123456",
            "email":"user@example.com",
            "Phone":"12345678"
    

        }}
