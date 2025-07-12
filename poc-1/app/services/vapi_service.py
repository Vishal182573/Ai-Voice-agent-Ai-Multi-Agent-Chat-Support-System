import httpx
from app.core.config import VAPI_API_KEY, VAPI_ASSISTANT_ID

VAPI_API_URL = "https://api.vapi.ai"

class VapiService:
    async def initiate_outbound_call(self, phone_number: str, language: str) -> dict:
        headers = {
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "assistantId": VAPI_ASSISTANT_ID,
            "phoneNumberId": "8e1f5249-cf19-4124-8236-afaea4ba5f7e", # Get this from your Vapi dashboard
            "customer": {
                "number": phone_number,
            }
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{VAPI_API_URL}/call/phone", headers=headers, json=payload)
                response.raise_for_status() # Raise exception for bad status codes
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"HTTP error occurred: {e.response.text}")
                return {"error": str(e)}