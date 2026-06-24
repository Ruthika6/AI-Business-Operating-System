from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import database
import models
import schemas
from services import support_service

router = APIRouter()

# Setup templates relative to this file's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/support", response_class=HTMLResponse)
def get_support_page(request: Request, db: Session = Depends(database.get_db)):
    tickets = support_service.get_tickets(db)
    return templates.TemplateResponse("support.html", {
        "request": request,
        "tickets": tickets,
        "active_tab": "support"
    })

@router.get("/api/support/tickets", response_model=list[schemas.TicketResponse])
def get_tickets_api(db: Session = Depends(database.get_db)):
    return support_service.get_tickets(db)

@router.post("/api/support/tickets", response_model=schemas.TicketResponse)
def create_ticket_api(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    return support_service.create_ticket(db, ticket)

@router.post("/api/support/analyze", response_model=schemas.TicketAnalyzeResponse)
def analyze_ticket_api(req: schemas.TicketAnalyzeRequest, db: Session = Depends(database.get_db)):
    # Scoring/classification endpoint
    from services import gemini_service
    details = {
        "customerName": req.customerName,
        "subject": req.subject,
        "message": req.message,
        "category": req.category
    }
    res = gemini_service.analyze_ticket(details)
    return res

@router.post("/api/support/analyze/{ticket_id}", response_model=schemas.TicketResponse)
def analyze_saved_ticket_api(ticket_id: int, db: Session = Depends(database.get_db)):
    res = support_service.analyze_ticket(db, ticket_id)
    if not res:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return res

@router.post("/api/support/reply", response_model=schemas.TicketReplyResponse)
def chatbot_reply_api(req: schemas.TicketReplyRequest):
    # Chatbot messages endpoint (takes messages list and returns chatbot text)
    reply_text = support_service.run_chatbot(req.messages)
    return {"message": reply_text}
