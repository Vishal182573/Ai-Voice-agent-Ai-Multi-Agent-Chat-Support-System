from sqlalchemy import Column, Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class CallLog(Base):
    __tablename__ = "call_logs"
    id = Column(Integer, primary_key=True, index=True)
    vapi_call_id = Column(String, unique=True, index=True)
    direction = Column(String) # "inbound" or "outbound"
    caller_number = Column(String)
    status = Column(String, default="initiated") # e.g., initiated, in-progress, completed, failed
    transcript = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ticket = relationship("ActionableTicket", back_populates="call", uselist=False)

class ActionableTicket(Base):
    __tablename__ = "actionable_tickets"
    id = Column(Integer, primary_key=True, index=True)
    call_log_id = Column(Integer, ForeignKey("call_logs.id"))
    intent = Column(String) # e.g., "Schedule Callback", "Resolve Issue", "Live Agent Request"
    summary = Column(Text)
    status = Column(String, default="Open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    call = relationship("CallLog", back_populates="ticket")