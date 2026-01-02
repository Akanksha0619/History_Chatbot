from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str = Field(
        ...,
        example="user_123"
    )
    message: str = Field(
        ...,
        example="My name is Akanksha"
    )
    conversation_id: Optional[str] = Field(
        None,
        example="1"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "What is my name?",
                "conversation_id": "1"
            }
        }
