from fastapi import APIRouter, Depends, Request, HTTPException, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import os
import database
import models
import schemas
from services import analytics_service

router = APIRouter()

# Setup templates relative to this file's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/analytics", response_class=HTMLResponse)
def get_analytics_page(request: Request, db: Session = Depends(database.get_db)):
    reports = db.query(models.AnalyticsReport).order_by(models.AnalyticsReport.uploaded_at.desc()).all()
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "reports": reports,
        "active_tab": "analytics"
    })

@router.post("/api/analytics/upload")
async def upload_csv_api(
    file: UploadFile = File(...), 
    db: Session = Depends(database.get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
    try:
        contents = await file.read()
        # Decode as utf-8, fallback to latin-1 if needed
        try:
            csv_text = contents.decode("utf-8")
        except UnicodeDecodeError:
            csv_text = contents.decode("latin-1")
            
        filename = file.filename
        
        result = analytics_service.generate_insights_from_csv(
            db=db, 
            csv_text=csv_text, 
            filename=filename
        )
        return result
    except Exception as e:
        print(f"Error handling CSV upload: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process CSV file: {str(e)}")

@router.post("/api/analytics/insights", response_model=schemas.CSVAnalyzeResponse)
def get_custom_insights_api(req: schemas.CSVAnalyzeRequest):
    # Generates custom insights for data
    from services import gemini_service
    res = gemini_service.generate_csv_insights(req.csvData, req.question)
    return res
