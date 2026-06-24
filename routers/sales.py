from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import database
import models
import schemas
from services import sales_service

router = APIRouter()

# Setup templates relative to this file's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/sales", response_class=HTMLResponse)
def get_sales_page(request: Request, db: Session = Depends(database.get_db)):
    leads = sales_service.get_leads(db)
    return templates.TemplateResponse("sales.html", {
        "request": request,
        "leads": leads,
        "active_tab": "sales"
    })

@router.get("/api/sales/leads", response_model=list[schemas.LeadResponse])
def get_leads_api(db: Session = Depends(database.get_db)):
    return sales_service.get_leads(db)

@router.post("/api/sales/leads", response_model=schemas.LeadResponse)
def create_lead_api(lead: schemas.LeadCreate, db: Session = Depends(database.get_db)):
    return sales_service.create_lead(db, lead)

@router.post("/api/sales/score", response_model=schemas.LeadScoreResponse)
def score_lead_api(req: schemas.LeadScoreRequest, db: Session = Depends(database.get_db)):
    # The request body is a json containing leadDetails dictionary
    details = req.leadDetails
    
    # We can either score a transient lead or update a lead if ID is passed
    # Let's support scoring transient lead details directly
    from services import gemini_service
    res = gemini_service.score_lead(details)
    return res

@router.post("/api/sales/score/{lead_id}")
def score_saved_lead_api(lead_id: int, db: Session = Depends(database.get_db)):
    res = sales_service.score_lead(db, lead_id)
    if not res:
        raise HTTPException(status_code=404, detail="Lead not found")
    return res

@router.post("/api/sales/email", response_model=schemas.LeadEmailResponse)
def generate_email_api(req: schemas.LeadEmailRequest):
    email_text = sales_service.generate_outreach_email(req)
    return {"email": email_text}
