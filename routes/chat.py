from fastapi import APIRouter
from models.chat import ChatReq
from utils.chat import handle_chat

router = APIRouter()


@router.post("/")
def chat(req: ChatReq):
    return handle_chat(req)
