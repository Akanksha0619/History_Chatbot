from fastapi import FastAPI
from handlers.user import router as user_router
from handlers.chat import router as chat_router
from handlers.auth import router as auth_router


app = FastAPI(title="History Based Chatbot")

@app.get("/")
def home():
    return {"Message": "Running"}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
