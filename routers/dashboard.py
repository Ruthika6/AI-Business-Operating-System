from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import database
import models
import schemas
from services import gemini_service

router = APIRouter()

# Setup templates relative to this file's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
def get_dashboard_page(request: Request, db: Session = Depends(database.get_db)):
    # Retrieve some basic info for Jinja2 rendering if needed
    metrics = db.query(models.RevenueMetric).all()
    leads = db.query(models.Lead).order_by(models.Lead.created_at.desc()).limit(5).all()
    tickets = db.query(models.SupportTicket).order_by(models.SupportTicket.created_at.desc()).limit(5).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "metrics": metrics,
        "leads": leads,
        "tickets": tickets,
        "active_tab": "dashboard"
    })

@router.get("/api/dashboard", response_model=schemas.DashboardResponse)
def get_dashboard_api(db: Session = Depends(database.get_db)):
    # Calculate SaaS metrics
    metrics = db.query(models.RevenueMetric).all()
    
    # Defaults in case DB metrics are empty
    total_rev = sum(m.revenue for m in metrics) if metrics else 248500.0
    mrr = metrics[-1].revenue if metrics else 32400.0
    cac = 180.0
    ltv = 2400.0
    conv_rate = 3.8
    active_custs = db.query(models.Lead).filter(models.Lead.status == "Qualified").count()
    if active_custs == 0:
        active_custs = 142
        
    metric_group = {
        "totalRevenue": total_rev,
        "monthlyRecurringRevenue": mrr,
        "customerAcquisitionCost": cac,
        "customerLifetimeValue": ltv,
        "conversionRate": conv_rate,
        "activeCustomers": active_custs
    }
    
    # Revenue history
    history = []
    for m in metrics:
        history.append({
            "month": m.month,
            "revenue": m.revenue,
            "target": m.target,
            "leads": m.leads_count
        })
        
    # If history is empty, return default mock history
    if not history:
        history = [
            {"month": "Jan", "revenue": 18200, "target": 17000, "leads": 110},
            {"month": "Feb", "revenue": 20400, "target": 19000, "leads": 140},
            {"month": "Mar", "revenue": 22100, "target": 21000, "leads": 165},
            {"month": "Apr", "revenue": 24800, "target": 23000, "leads": 198},
            {"month": "May", "revenue": 29500, "target": 26000, "leads": 220},
            {"month": "Jun", "revenue": 32400, "target": 30000, "leads": 285}
        ]
        
    # Leads list
    leads = db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()
    
    # Tickets list
    tickets = db.query(models.SupportTicket).order_by(models.SupportTicket.created_at.desc()).all()
    
    # Meetings list
    meetings = db.query(models.Meeting).order_by(models.Meeting.created_at.desc()).all()
    
    # Recommendations
    recommendations_db = db.query(models.Recommendation).all()
    recommendations = []
    for r in recommendations_db:
        recommendations.append({
            "id": r.id,
            "title": r.title,
            "category": r.category,
            "impact": r.impact,
            "description": r.description,
            "actionable_step": r.actionable_step
        })
        
    if not recommendations:
        # Generate mock suggestions
        recommendations = gemini_service.generate_business_recommendations()
        
    return {
        "metrics": metric_group,
        "revenueHistory": history,
        "leads": leads,
        "tickets": tickets,
        "meetings": meetings,
        "recommendations": recommendations
    }

@router.post("/api/copilot/query", response_model=schemas.CopilotQueryResponse)
def copilot_query(req: schemas.CopilotQueryRequest, db: Session = Depends(database.get_db)):
    # Build contexts
    metrics = db.query(models.RevenueMetric).all()
    total_rev = sum(m.revenue for m in metrics) if metrics else 248500.0
    mrr = metrics[-1].revenue if metrics else 32400.0
    
    metrics_ctx = f"Total Revenue: ${total_rev}, MRR: ${mrr}, Active Clients: 142, CAC: $180, LTV: $2400"
    
    leads = db.query(models.Lead).limit(5).all()
    leads_ctx = ", ".join([f"{l.name} ({l.company}, score: {l.score}, status: {l.status})" for l in leads])
    
    tickets = db.query(models.SupportTicket).limit(5).all()
    tickets_ctx = ", ".join([f"{t.customer_name}: {t.subject} ({t.priority}, status: {t.status})" for t in tickets])
    
    answer = gemini_service.generate_executive_summary(
        question=req.question,
        metrics_context=metrics_ctx,
        leads_context=leads_ctx,
        support_context=tickets_ctx
    )
    
    model_used = "gemini-2.5-flash" if os.environ.get("GEMINI_API_KEY") else "Simulated Strategic LLM"
    
    return {
        "answer": answer,
        "model": model_used
    }
