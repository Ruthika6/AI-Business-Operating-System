from sqlalchemy.orm import Session
import models
import schemas
from services import gemini_service
import datetime

def get_meetings(db: Session):
    return db.query(models.Meeting).order_by(models.Meeting.created_at.desc()).all()

def get_meeting(db: Session, meeting_id: int):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()

def toggle_action_item(db: Session, item_id: int):
    item = db.query(models.ActionItem).filter(models.ActionItem.id == item_id).first()
    if item:
        item.status = "Completed" if item.status == "Pending" else "Pending"
        db.commit()
        db.refresh(item)
    return item

def summarize_and_create_meeting(db: Session, transcript: str, title: str):
    # Call Gemini to get summary and action items
    analysis = gemini_service.summarize_meeting(transcript, title)
    
    # Save the meeting
    meeting_title = title or "Sales Sync & Operational Alignment"
    meeting_date = datetime.datetime.now().strftime("%Y-%m-%d")
    meeting_duration = "45 mins"  # default
    
    # Check if we can infer duration from transcript
    if "mins" in transcript or "minutes" in transcript:
        # Simple regex to search for duration
        import re
        match = re.search(r'(\d+)\s*(?:mins|minutes)', transcript, re.IGNORECASE)
        if match:
            meeting_duration = f"{match.group(1)} mins"

    db_meeting = models.Meeting(
        title=meeting_title,
        date=meeting_date,
        duration=meeting_duration,
        raw_transcript=transcript,
        summary=analysis.get("summary", "Summary pending...")
    )
    
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    
    # Save action items
    action_items = []
    for item in analysis.get("actionItems", []):
        db_item = models.ActionItem(
            meeting_id=db_meeting.id,
            text=item.get("text", "Action item"),
            assignee=item.get("assignee", "Unassigned"),
            due_date=item.get("dueDate", meeting_date),
            status=item.get("status", "Pending")
        )
        db.add(db_item)
        action_items.append(db_item)
        
    db.commit()
    db.refresh(db_meeting)
    
    return db_meeting
