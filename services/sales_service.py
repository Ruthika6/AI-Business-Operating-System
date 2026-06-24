from sqlalchemy.orm import Session
import models
import schemas
from services import gemini_service

def get_leads(db: Session):
    return db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id).first()

def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(
        name=lead.name,
        company=lead.company,
        email=lead.email,
        segment=lead.segment,
        notes=lead.notes,
        score=lead.score,
        status=lead.status,
        sentiment=lead.sentiment
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def score_lead(db: Session, lead_id: int):
    db_lead = get_lead(db, lead_id)
    if not db_lead:
        return None
        
    lead_details = {
        "name": db_lead.name,
        "company": db_lead.company,
        "email": db_lead.email,
        "segment": db_lead.segment,
        "notes": db_lead.notes or ""
    }
    
    score_result = gemini_service.score_lead(lead_details)
    
    # Update lead in database
    db_lead.score = score_result.get("score", 50)
    db_lead.sentiment = score_result.get("category", "Warm Lead (Tier 2)")
    
    db.commit()
    db.refresh(db_lead)
    
    return {
        "lead": db_lead,
        "scoring_details": score_result
    }

def generate_outreach_email(email_req: schemas.LeadEmailRequest):
    details = {
        "leadName": email_req.leadName,
        "company": email_req.company,
        "segment": email_req.segment,
        "purpose": email_req.purpose,
        "notes": email_req.notes
    }
    email_text = gemini_service.generate_sales_email(details)
    return email_text
