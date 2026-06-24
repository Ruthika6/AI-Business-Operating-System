from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    company = Column(String, nullable=True)
    email = Column(String, nullable=True)
    segment = Column(String, nullable=True)  # Enterprise, Mid-Market, SMB, Startup
    notes = Column(Text, nullable=True)
    score = Column(Integer, default=50)
    status = Column(String, default="New")   # New, Contacted, Qualified, Closed
    sentiment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    subject = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    priority = Column(String, default="Medium")  # Low, Medium, High, Critical
    status = Column(String, default="Open")      # Open, In Progress, Resolved
    ai_suggested_response = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=True)      # YYYY-MM-DD
    duration = Column(String, nullable=True)  # e.g., "45 mins"
    raw_transcript = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")

class ActionItem(Base):
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    text = Column(Text, nullable=False)
    assignee = Column(String, nullable=True)
    due_date = Column(String, nullable=True)  # YYYY-MM-DD
    status = Column(String, default="Pending") # Pending, Completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    meeting = relationship("Meeting", back_populates="action_items")

class RevenueMetric(Base):
    __tablename__ = "revenue_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, nullable=False)  # e.g., "Jan", "Feb"
    revenue = Column(Float, nullable=False)
    target = Column(Float, nullable=False)
    leads_count = Column(Integer, default=0)
    active_customers = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)  # Revenue, Support, Sales, Operations
    impact = Column(String, nullable=True)    # High, Medium, Low
    description = Column(Text, nullable=True)
    actionable_step = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    analysis_result = Column(Text, nullable=True)
    chart_data_json = Column(Text, nullable=True)  # JSON string format
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
