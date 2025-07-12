from fastapi import FastAPI
from app.api.endpoints import outbound, webhooks
from app.db import models
from app.db.database import engine

# Create all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PoC-1: AI Voice Agent System",
    description="An AI voice assistant for inbound and outbound calls using Vapi, FastAPI, and Gemini.",
    version="1.0.0"
)

app.include_router(outbound.router, prefix="/outbound", tags=["Outbound Calls"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Vapi Webhooks"])

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "AI Voice Agent System is running. Visit /docs for API details."}