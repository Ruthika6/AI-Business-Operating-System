from sqlalchemy.orm import Session
import models
import schemas
from services import gemini_service

def get_tickets(db: Session):
    return db.query(models.SupportTicket).order_by(models.SupportTicket.created_at.desc()).all()

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.SupportTicket).filter(models.SupportTicket.id == ticket_id).first()

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.SupportTicket(
        customer_name=ticket.customer_name,
        email=ticket.email,
        subject=ticket.subject,
        message=ticket.message,
        category=ticket.category,
        priority=ticket.priority,
        status=ticket.status,
        ai_suggested_response=ticket.ai_suggested_response,
        sentiment=ticket.sentiment
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def analyze_ticket(db: Session, ticket_id: int):
    db_ticket = get_ticket(db, ticket_id)
    if not db_ticket:
        return None
        
    details = {
        "customerName": db_ticket.customer_name,
        "subject": db_ticket.subject or "No Subject",
        "message": db_ticket.message,
        "category": db_ticket.category or ""
    }
    
    analysis = gemini_service.analyze_ticket(details)
    
    # Update DB fields
    db_ticket.priority = analysis.get("priority", "Medium")
    db_ticket.sentiment = analysis.get("sentiment", "Neutral")
    db_ticket.category = analysis.get("category", "General Support")
    db_ticket.ai_suggested_response = analysis.get("suggestedReply", "")
    
    db.commit()
    db.refresh(db_ticket)
    
    return db_ticket

def run_chatbot(messages: list):
    # Format messages for the Gemini service (checking roles and contents)
    formatted = []
    for msg in messages:
        formatted.append({
            "role": "user" if msg.get("role") == "user" else "model",
            "content": msg.get("content", "")
        })
    reply = gemini_service.generate_support_reply(formatted)
    return reply
