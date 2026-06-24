import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import models

# Import routers
from routers import dashboard, sales, support, meeting, analytics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FlowZint AI Business Operating System",
    description="Intelligent SaaS Operating System powered by Gemini AI",
    version="1.0.0"
)

# CORS middleware config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve paths dynamically relative to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Mount static folder (directories must already exist in repo)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(dashboard.router)
app.include_router(sales.router)
app.include_router(support.router)
app.include_router(meeting.router)
app.include_router(analytics.router)

# --- DATABASE SEEDER ---
def seed_database():
    db = SessionLocal()
    try:
        # Check if DB is already seeded
        if db.query(models.RevenueMetric).first() is not None:
            return
            
        print("Database is empty. Seeding initial corporate data...")
        
        # 1. Seed Revenue History (Jan - Jun)
        revenue_data = [
            models.RevenueMetric(month="Jan", revenue=18200.0, target=17000.0, leads_count=110, active_customers=95),
            models.RevenueMetric(month="Feb", revenue=20400.0, target=19000.0, leads_count=140, active_customers=108),
            models.RevenueMetric(month="Mar", revenue=22100.0, target=21000.0, leads_count=165, active_customers=115),
            models.RevenueMetric(month="Apr", revenue=24800.0, target=23000.0, leads_count=198, active_customers=124),
            models.RevenueMetric(month="May", revenue=29500.0, target=26000.0, leads_count=220, active_customers=132),
            models.RevenueMetric(month="Jun", revenue=32400.0, target=30000.0, leads_count=285, active_customers=142),
        ]
        db.add_all(revenue_data)
        
        # 2. Seed Initial CRM Leads
        leads_data = [
            models.Lead(
                name="Sarah Jenkins",
                company="Apex Global",
                email="sarah@apexgl.com",
                segment="Enterprise",
                notes="Met at TechCrunch. High budget. Needs custom CRM integration and security audit details.",
                score=85,
                status="Qualified",
                sentiment="Positive"
            ),
            models.Lead(
                name="Marcus Vance",
                company="Innovate Labs",
                email="marcus@innovatelabs.io",
                segment="Mid-Market",
                notes="Interested in scaling API pipelines. Requests custom staging/sandbox trial environment.",
                score=92,
                status="Qualified",
                sentiment="Positive"
            ),
            models.Lead(
                name="Tariq Mahmood",
                company="ByteSized Inc",
                email="tariq@bytesized.co",
                segment="SMB",
                notes="Small team, looking to automate invoice alerts and tickets categorization.",
                score=45,
                status="New",
                sentiment="Neutral"
            ),
            models.Lead(
                name="Elena Rostova",
                company="Nova Ventures",
                email="elena@novaventures.com",
                segment="Startup",
                notes="Exploring cost-saving setups. Expressed CAC concerns during initial discovery call.",
                score=68,
                status="Contacted",
                sentiment="Neutral"
            )
        ]
        db.add_all(leads_data)
        
        # 3. Seed Support Tickets
        tickets_data = [
            models.SupportTicket(
                customer_name="David Kim",
                email="david@kimtech.net",
                subject="API Integration Error - Invalid Endpoint Signature",
                message="We are consistently receiving a 403 authorization signature mismatch when attempting to register webhooks via the enterprise API portal under v2 endpoints. This is blocking our core production launch of our integration schedules. Can you escalate this asap?",
                category="Technical API",
                priority="Critical",
                status="Open",
                sentiment="Negative",
                ai_suggested_response=(
                    "Dear David,\n\nThank you for reaching out. We have flagged this webhook v2 signature issue with priority. "
                    "Our engineering team is actively investigating the authorization header verification sequence. "
                    "I will provide an update within the hour with a resolution details."
                )
            ),
            models.SupportTicket(
                customer_name="Lara Croft",
                email="lara@tombadventures.org",
                subject="Billing Query: Annual Subscription Invoice Duplicate",
                message="Hello, I noticed that our company credit card was charged twice on June 15th for our annual scale tier upgrade. We received two identical invoices: INV-2026-4402 and INV-2026-4403. Please refund one of them as soon as possible.",
                category="Billing",
                priority="High",
                status="In Progress",
                sentiment="Neutral",
                ai_suggested_response=(
                    "Dear Lara,\n\nI apologize for the double billing error. "
                    "I have located invoices INV-2026-4402 and INV-2026-4403. "
                    "I am initiating a refund for invoice INV-2026-4403 immediately. "
                    "The credit should post back to your account in 3-5 business days."
                )
            ),
            models.SupportTicket(
                customer_name="Frank Miller",
                email="frank@millermedia.com",
                subject="UI Bug: Dashboard graph legend mismatch on dark mode",
                message="Just a small cosmetic bug: in the latest UI release, the custom line chart legends are turning charcoal-grey when switching to dark mode, making them completely unreadable against standard cards. Otherwise, loving the operating system!",
                category="UI Cosmetic",
                priority="Low",
                status="Resolved",
                sentiment="Positive",
                ai_suggested_response=(
                    "Dear Frank,\n\nThank you for reporting this UI visual bug. "
                    "We have updated the CSS configuration for dark-mode chart legends. "
                    "The change is deployed in the latest hotfix, and legends should now render clearly."
                )
            )
        ]
        db.add_all(tickets_data)
        
        # 4. Seed Meeting Transcript and Summary
        meeting = models.Meeting(
            title="Quarterly Marketing Sync & Sales Prep",
            date="2026-06-24",
            duration="45 mins",
            raw_transcript=(
                "John (Sales Lead): Hey team, let's align on next week's campaign. We have about 180 hot inbound leads coming from the TechCrunch mention, but we need dynamic emails generated and clear assignments.\n"
                "Alice (Marketing Director): Agreed. I've drafted some content assets but need help summarizing the target customer segmentation. We should target Enterprise and Mid-Market heavily. Sarah Jenkins from Apex Global is waiting on an updated ROI prospectus.\n"
                "John: Got it. I'll take Sarah's email and generate a tailored sales prospectus. Bob, can you handle Marcus's custom trial walkthrough configuration?\n"
                "Bob (Support Engineer): Yeah, I can set up Innovate Labs' trial sandbox by Monday morning. I'll need current API schema versions.\n"
                "John: Awesome. Let's make sure we have that sandbox done. Alice, you'll publish the TechCrunch case study by Friday afternoon as a trust-signal resource."
            ),
            summary=(
                "The team aligned on campaign preparation following a TechCrunch feature. "
                "The focus is on Enterprise and Mid-Market inbound targets, with specific tasks allocated for VIP high-score leads."
            )
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        
        # 5. Seed Meeting Action Items
        action_items = [
            models.ActionItem(
                meeting_id=meeting.id,
                text="Publish TechCrunch client case study on the resource page",
                assignee="Alice",
                due_date="2026-06-26",
                status="Pending"
            ),
            models.ActionItem(
                meeting_id=meeting.id,
                text="Create custom sandbox walkthrough environment for Innovate Labs trial support",
                assignee="Bob",
                due_date="2026-06-29",
                status="Completed"
            ),
            models.ActionItem(
                meeting_id=meeting.id,
                text="Draft tailored enterprise sales prospectus and email target",
                assignee="John",
                due_date="2026-06-25",
                status="Pending"
            )
        ]
        db.add_all(action_items)
        
        # 6. Seed CEO Recommendations
        recommendations = [
            models.Recommendation(
                title="Optimize Customer Acquisition Cost (CAC)",
                category="Revenue",
                impact="High",
                description="Organic traffic increased by 35% this quarter, but paid search ads show diminishing returns. Reallocating budget creates immediate cost-savings.",
                actionable_step="Shift $5,000/mo search marketing budget to developer relations and target inbound SEO marketing content modules."
            ),
            models.Recommendation(
                title="Escalate Critical Support Webhook Bugs",
                category="Support",
                impact="High",
                description="API authorization signature bugs are affecting 3 high-lifetime-value enterprise accounts, risking client acquisition and trust.",
                actionable_step="Assign senior staff to verify enterprise webhook authorization schemas and update API error handling responses."
            ),
            models.Recommendation(
                title="Nurture Active Enterprise Prospect Leads",
                category="Sales",
                impact="Medium",
                description="Prospects like Marcus Vance (Innovate Labs) and Sarah Jenkins (Apex Global) have scores >80% and are primary targets for sales conversion.",
                actionable_step="Generate personalized sales pitches offering an extended trial sandbox alongside pre-configured templates."
            )
        ]
        db.add_all(recommendations)
        
        db.commit()
        print("Database successfully seeded with default data.")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

# Run database seeding
seed_database()

if __name__ == "__main__":
    import uvicorn
    from config import PORT
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
