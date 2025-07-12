from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse
from app.agents.intent_classifier_agent import IntentClassifierAgent
from app.agents.routing_agent import AgentRouter
from app.agents.support_agent import SupportAgent
from app.agents.notify_agent import NotifyAgent

router = APIRouter()

intent_agent = IntentClassifierAgent()
notify_agent = NotifyAgent()

@router.post("/chat", response_model=ChatQueryResponse)
async def handle_chat_query(
    request: ChatQueryRequest,
    db: Session = Depends(get_db)
):
    # 1. Classify intent using the Gemini-powered agent 
    intent = intent_agent.classify_intent(request.query)

    # 2. Initialize agents that need the DB session
    support_agent = SupportAgent(db_session=db)
    routing_agent = AgentRouter(support_agent)

    # 3. Route to the correct support agent to get a response 
    response_text = routing_agent.route(intent=intent, query=request.query)

    # 4. Log the entire conversation to the database 
    log_entry = models.MessageLog(
        user_query=request.query,
        detected_intent=intent,
        bot_response=response_text
    )
    db.add(log_entry)
    db.commit()

    # 5. If it was a complaint, trigger a notification 
    if intent == "Complaint":
        notify_agent.send_update(f"New complaint ticket created for query: '{request.query}'")

    return ChatQueryResponse(response=response_text, intent=intent)