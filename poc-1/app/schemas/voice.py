from pydantic import BaseModel
from typing import Optional

class OutboundCallRequest(BaseModel):
    phone_number: str
    language: Optional[str] = 'en' # Optional language support

class VapiWebhookPayload(BaseModel):
    # A simplified model. Vapi sends much more.
    # We use a dictionary to handle the flexible message structure.
    message: dict