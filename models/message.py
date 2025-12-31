from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    conversation_id: str
    role: str           
    content: str


class MessageResponse(BaseModel):
    role: str
    content: str
    timestamp: str
