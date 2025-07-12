from pydantic import BaseModel

# Schema for the incoming request body
class ChatQueryRequest(BaseModel):
    query: str

# Schema for the outgoing response body
class ChatQueryResponse(BaseModel):
    response: str
    intent: str