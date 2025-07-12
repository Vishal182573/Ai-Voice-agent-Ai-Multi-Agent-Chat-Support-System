from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.services.analysis_service import AnalysisService

router = APIRouter()
analysis_service = AnalysisService()

@router.post("/vapi")
async def handle_vapi_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    payload = await request.json()
    message = payload.get("message", {})
    message_type = message.get("type")
    call_data = message.get("call", {})
    vapi_call_id = call_data.get("id")

    if not vapi_call_id:
        return {"status": "ignoring, no call id"}

    # Find the corresponding call log
    call_log = db.query(models.CallLog).filter(models.CallLog.vapi_call_id == vapi_call_id).first()
    if not call_log:
         # For inbound calls, the log won't exist yet. Create it.
        if message_type == "call-start":
            call_log = models.CallLog(
                vapi_call_id=vapi_call_id,
                direction="inbound",
                caller_number=call_data.get("customer", {}).get("number"),
                status="in-progress"
            )
            db.add(call_log)
            db.commit()
            db.refresh(call_log)
        else:
             raise HTTPException(status_code=404, detail="Call log not found")


    # Handle different event types from Vapi
    if message_type == "call-start":
        call_log.status = "in-progress"

    elif message_type == "transcript":
        transcript_part = message.get("transcript", "")
        if transcript_part:
            call_log.transcript += transcript_part + "\n"

    elif message_type == "call-end":
        call_log.status = "completed"
        db.commit() # Commit status before analysis

        # Analyze the full transcript to create a ticket
        analysis_result = analysis_service.extract_intent_from_transcript(call_log.transcript)
        new_ticket = models.ActionableTicket(
            call_log_id=call_log.id,
            intent=analysis_result.get("intent"),
            summary=analysis_result.get("summary"),
        )
        db.add(new_ticket)

    db.commit()
    return {"status": "success"}