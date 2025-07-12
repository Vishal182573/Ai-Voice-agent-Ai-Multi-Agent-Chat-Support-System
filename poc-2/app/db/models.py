from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class MessageLog(Base):
    __tablename__ = "message_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_query = Column(String)
    detected_intent = Column(String)
    bot_response = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_query = Column(String)
    status = Column(String, default="Open")