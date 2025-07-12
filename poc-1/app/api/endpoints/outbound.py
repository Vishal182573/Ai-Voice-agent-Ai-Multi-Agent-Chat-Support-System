from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas.voice import OutboundCallRequest
from app.services.vapi_service import VapiService

router = APIRouter()
vapi_service = VapiService()

@router.post("/call")
async def trigger_outbound_call(
    request: OutboundCallRequest,
    db: Session = Depends(get_db)
):
    vapi_response = await vapi_service.initiate_outbound_call(
        phone_number=request.phone_number,
        language=request.language
    )

    if "error" in vapi_response or "id" not in vapi_response:
        raise HTTPException(status_code=500, detail=f"Failed to initiate call: {vapi_response.get('error', 'Unknown error')}")

    # Log the initiated call in the database
    new_call = models.CallLog(
        vapi_call_id=vapi_response["id"],
        direction="outbound",
        caller_number=request.phone_number,
        status="initiated"
    )
    db.add(new_call)
    db.commit()
    db.refresh(new_call)

    return {"message": "Outbound call initiated successfully", "call_id": new_call.id}