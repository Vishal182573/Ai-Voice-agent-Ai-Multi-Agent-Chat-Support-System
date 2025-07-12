from fastapi import FastAPI
from app.api.endpoints import chat
from app.db import models
from app.db.database import engine

# This command creates all the database tables defined in app/db/models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PoC-2: AI Multi-Agent Chat Support System",
    description="A multi-agent chat system using FastAPI and Gemini.",
    version="1.0.0"
)

# Include the chat API router
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the AI Multi-Agent Chat Support System. Visit /docs for the API."}