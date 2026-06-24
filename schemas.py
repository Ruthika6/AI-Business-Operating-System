from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Common Schema ---
class ConfigBase(BaseModel):
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(ConfigBase):
    email: EmailStr
    username: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

# --- Lead Schemas ---
class LeadBase(ConfigBase):
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    segment: Optional[str] = None
    notes: Optional[str] = None
    score: Optional[int] = 50
    status: Optional[str] = "New"
    sentiment: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    created_at: datetime

class LeadScoreRequest(BaseModel):
    leadDetails: dict

class LeadScoreResponse(BaseModel):
    score: int
    category: str
    positives: List[str]
    concerns: List[str]
    recommendation: str

class LeadEmailRequest(BaseModel):
    leadName: str
    company: str
    email: Optional[str] = None
    segment: Optional[str] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None

class LeadEmailResponse(BaseModel):
    email: str

# --- Support Ticket Schemas ---
class TicketBase(ConfigBase):
    customer_name: str
    email: Optional[str] = None
    subject: Optional[str] = None
    message: str
    category: Optional[str] = None
    priority: Optional[str] = "Medium"
    status: Optional[str] = "Open"
    ai_suggested_response: Optional[str] = None
    sentiment: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketResponse(TicketBase):
    id: int
    created_at: datetime

class TicketAnalyzeRequest(BaseModel):
    customerName: Optional[str] = None
    message: str
    subject: Optional[str] = None
    category: Optional[str] = None

class TicketAnalyzeResponse(BaseModel):
    priority: str
    sentiment: str
    category: str
    suggestedReply: str

class TicketReplyRequest(BaseModel):
    messages: List[dict]

class TicketReplyResponse(BaseModel):
    message: str

# --- Meeting Schemas ---
class ActionItemBase(ConfigBase):
    text: str
    assignee: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = "Pending"

class ActionItemCreate(ActionItemBase):
    pass

class ActionItemResponse(ActionItemBase):
    id: int
    meeting_id: int
    created_at: datetime

class MeetingBase(ConfigBase):
    title: str
    date: Optional[str] = None
    duration: Optional[str] = None
    raw_transcript: str
    summary: Optional[str] = None

class MeetingCreate(MeetingBase):
    pass

class MeetingResponse(MeetingBase):
    id: int
    created_at: datetime
    action_items: List[ActionItemResponse] = []

class MeetingSummarizeRequest(BaseModel):
    transcript: str
    title: Optional[str] = None

class MeetingSummarizeResponse(BaseModel):
    summary: str
    actionItems: List[dict]

# --- Analytics Schemas ---
class ForecastDataPoint(BaseModel):
    month: str
    revenue: float

class CSVAnalyzeRequest(BaseModel):
    csvData: str
    question: Optional[str] = None

class CSVAnalyzeResponse(BaseModel):
    analysis: str
    forecastData: List[ForecastDataPoint]

# --- CEO Copilot / Dashboard Schemas ---
class CopilotQueryRequest(BaseModel):
    question: str

class CopilotQueryResponse(BaseModel):
    answer: str
    model: str

class RevenueHistoryPoint(ConfigBase):
    month: str
    revenue: float
    target: float
    leads: int

class DashboardMetricGroup(BaseModel):
    totalRevenue: float
    monthlyRecurringRevenue: float
    customerAcquisitionCost: float
    customerLifetimeValue: float
    conversionRate: float
    activeCustomers: int

class DashboardResponse(BaseModel):
    metrics: DashboardMetricGroup
    revenueHistory: List[RevenueHistoryPoint]
    leads: List[LeadResponse]
    tickets: List[TicketResponse]
    meetings: List[MeetingResponse]
    recommendations: List[dict]
