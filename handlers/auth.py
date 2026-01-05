from fastapi import APIRouter
from models.auth import LoginRequest
from utils.auth import login_user

router = APIRouter()


@router.post("/login")
def login(req: LoginRequest):
    return login_user(req.email, req.password)
