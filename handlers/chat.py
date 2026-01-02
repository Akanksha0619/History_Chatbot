from fastapi import APIRouter
from models.chat import ChatRequest
from utils.chat import process_chat

router = APIRouter()


@router.post("/")
def chat(req: ChatRequest):
    return process_chat(
        user_id=req.user_id,
        message=req.message,
        conversation_id=req.conversation_id
    )
