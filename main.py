from fastapi import FastAPI
from routes.user import router as user_router
from routes.chat import router as chat_router

app = FastAPI(title="History Based Chatbot")

@app.get("/")
def home():
    return {"Message : Running"}

app.include_router(user_router)
app.include_router(chat_router)
