from pydantic import BaseModel
from typing import Optional

class ChatReq(BaseModel):
    user_id: str
    message: str
    conversation_id: Optional[str] = None
