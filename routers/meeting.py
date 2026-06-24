from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import database
import models
import schemas
from services import meeting_service

router = APIRouter()

# Setup templates relative to this file's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/meetings", response_class=HTMLResponse)
def get_meetings_page(request: Request, db: Session = Depends(database.get_db)):
    meetings = meeting_service.get_meetings(db)
    return templates.TemplateResponse("meetings.html", {
        "request": request,
        "meetings": meetings,
        "active_tab": "meetings"
    })

@router.get("/api/meeting/history", response_model=list[schemas.MeetingResponse])
def get_meetings_history_api(db: Session = Depends(database.get_db)):
    return meeting_service.get_meetings(db)

@router.post("/api/meeting/summarize", response_model=schemas.MeetingResponse)
def summarize_meeting_api(req: schemas.MeetingSummarizeRequest, db: Session = Depends(database.get_db)):
    if not req.transcript:
        raise HTTPException(status_code=400, detail="Transcript is required")
    db_meeting = meeting_service.summarize_and_create_meeting(db, req.transcript, req.title)
    return db_meeting

@router.post("/api/meeting/action-item/{item_id}/toggle")
def toggle_action_item_api(item_id: int, db: Session = Depends(database.get_db)):
    item = meeting_service.toggle_action_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return {"id": item.id, "status": item.status}
