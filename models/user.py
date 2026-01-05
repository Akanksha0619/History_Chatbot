from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2)
    password: str
    email: EmailStr
    phone: str
    role: Optional[str] = "user"


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = None

    
    class Config:
        json_schema_extra = {"example": {

            "name":"user",
            "password":"123456",
            "email":"user@example.com",
            "Phone":"12345678"
    

        }}
