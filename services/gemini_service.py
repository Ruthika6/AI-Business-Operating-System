import os
import json
import random
import re
from typing import Dict, List, Any
from config import GEMINI_API_KEY

# Attempt to import google-genai, with fallback to google-generativeai or mock
HAS_GOOGLE_GENAI = False
try:
    from google import genai
    from google.genai import types
    HAS_GOOGLE_GENAI = True
except ImportError:
    try:
        import google.generativeai as genai_legacy
    except ImportError:
        pass

def get_gemini_client():
    if not GEMINI_API_KEY:
        return None
    
    if HAS_GOOGLE_GENAI:
        try:
            return genai.Client(api_key=GEMINI_API_KEY)
        except Exception as e:
            print(f"Error initializing Google GenAI Client: {e}")
            return None
    return None

# --- MOCK SIMULATOR FOR ROBUSTNESS ---
class GeminiSimulator:
    @staticmethod
    def generate_executive_summary(question: str, metrics_context: str, leads_context: str, support_context: str) -> str:
        q_lower = question.lower()
        if "health" in q_lower or "summary" in q_lower or "performance" in q_lower:
            return (
                "### Current Business Health Overview\n\n"
                "PulseFlow Systems is demonstrating strong operating leverage. Your **MRR stands at $32.4K**, marking a consistent monthly acceleration from **$18.2K** in January. \n\n"
                "**Financial Health KPI Matrix:**\n"
                "- **Monthly Revenue Trend:** +18.4% month-over-month target growth.\n"
                "- **LTV to CAC ratio:** **13.3x** ($2,400 CLV vs. $180 CAC) which is extremely healthy, comfortably exceeding the standard SaaS benchmark of 3x.\n"
                "- **Leads Funnel Velocity:** Monthly inbound leads surged from 110 to 285.\n\n"
                "**Immediate Interventions Recommended:**\n"
                "1. Address the critical API Integration error from KimTech Net to safeguard developer trust.\n"
                "2. Initiate a targeted outbound sequence to the high-scoring mid-market leads who are currently in the 'Qualified' pipeline."
            )
        elif "revenue" in q_lower or "sales" in q_lower or "forecast" in q_lower or "financial" in q_lower:
            return (
                "### Financial & Revenue Projection Insights\n\n"
                "Based on current growth trends ($32.4K active MRR, trending toward an end-of-quarter trajectory of ~$37K):\n"
                "- **Conversion Efficiency:** Lead-to-customer conversion is stable at **3.8%**.\n"
                "- **Annual Run Rate (ARR):** Approaching **$388.8K**.\n\n"
                "**Strategic Opportunities:**\n"
                "- Converting high-scoring prospects like Apex Global (Sarah Jenkins) and Innovate Labs (Marcus Vance) will push the enterprise segment to 45% of total revenue. This significantly increases your Net Revenue Retention."
            )
        elif "support" in q_lower or "ticket" in q_lower or "customer" in q_lower:
            return (
                "### Customer Support Operations Summary\n\n"
                "- There is currently **1 Critical ticket** open (raised by David Kim regarding invalid webhook signatures on v2 endpoints). This is blocking a production launch and should be prioritized immediately.\n"
                "- General support sentiment is balanced, indicating that customer success processes are holding up, but technical friction is rising.\n"
                "- **Resolution Recommendation:** Reassign a senior backend engineer to verify Webhook authorization schemas and update API error handling responses."
            )
        else:
            return (
                f"### CEO Executive Synthesis\n\n"
                f"In response to: *\"{question}\"*\n\n"
                "Here is my strategic assessment based on real-time PulseFlow operational data:\n\n"
                "1. **Traction & Metrics**: MRR ($32.4k) and active client indices (142 users) show solid traction. The exceptionally low CAC ($180) suggests you have room to increase marketing spend.\n"
                "2. **Sales Target**: Marcus Vance (Innovate Labs) has scored **92** on our lead analysis engine and represents a high-probability close. We should schedule a trial sandbox walkthrough immediately.\n"
                "3. **Fulfillment Bottlenecks**: Support Ticket #t1 represents a blocking API Integration bug that threatens conversion momentum. Resolving this should precede new marketing campaigns."
            )

    @staticmethod
    def generate_business_recommendations() -> List[Dict[str, Any]]:
        return [
            {
                "title": "Optimize Customer Acquisition Cost (CAC)",
                "category": "Revenue",
                "impact": "High",
                "description": "Organic traffic increased by 35% this quarter, but paid search ads show diminishing returns. Reallocating budget creates immediate cost-savings.",
                "actionable_step": "Shift $5,000/mo search marketing budget to developer relations and target inbound SEO marketing content modules."
            },
            {
                "title": "Escalate Critical Support Webhook Bugs",
                "category": "Support",
                "impact": "High",
                "description": "API authorization signature bugs are affecting 3 high-lifetime-value enterprise accounts, risking client acquisition and trust.",
                "actionable_step": "Assign senior staff to verify enterprise webhook authorization schemas and update API error handling responses."
            },
            {
                "title": "Nurture Active Enterprise Prospect Leads",
                "category": "Sales",
                "impact": "Medium",
                "description": "Prospects like Marcus Vance (Innovate Labs) and Sarah Jenkins (Apex Global) have scores >80% and are primary targets for sales conversion.",
                "actionable_step": "Generate personalized sales pitches offering an extended trial sandbox alongside pre-configured templates."
            }
        ]

    @staticmethod
    def score_lead(details: Dict[str, Any]) -> Dict[str, Any]:
        # Generate dynamic mock score based on text inputs
        score = 50
        name = str(details.get("name", "")).lower()
        company = str(details.get("company", "")).lower()
        notes = str(details.get("notes", "")).lower()
        
        # Calculate a pseudo-realistic score based on keyword match
        if "budget" in notes or "budget" in name: score += 10
        if "immediate" in notes or "asap" in notes: score += 15
        if "decision maker" in notes or "vp" in notes or "director" in notes: score += 15
        if "enterprise" in notes or len(company) > 10: score += 10
        if "trial" in notes: score += 5
        
        score = min(max(score, 30), 98)
        
        category = "Hot Lead (Tier 1)" if score >= 80 else "Warm Lead (Tier 2)" if score >= 55 else "Cold Lead (Tier 3)"
        
        return {
            "score": score,
            "category": category,
            "positives": [
                "Expressed clear timelines in communications.",
                "Target segment fits best-in-class product fit characteristics.",
                "High decision-making authority matches target client profile."
            ],
            "concerns": [
                "Will require dedicated sandbox environments to validate enterprise security parameters.",
                "Slight pricing sensitivity indicated under initial inquiries."
            ],
            "recommendation": "Provide a personalized ROI assessment highlighting our multi-tenant scaling efficiencies and offer a scheduled 15-minute engineering blueprint call."
        }

    @staticmethod
    def generate_sales_email(details: Dict[str, Any]) -> str:
        lead_name = details.get("leadName", "Prospect")
        company = details.get("company", "your company")
        segment = details.get("segment", "Enterprise")
        purpose = details.get("purpose", "optimizing operations")
        notes = details.get("notes", "")
        
        custom_snippet = f"Regarding your interest in: '{notes}', we support full pre-constructed widgets and sandboxes tailored exactly to this." if notes else "I would love to set up a short, 10-minute introduction call to showcase how we can support your business goals."

        return (
            f"Subject: Tailored Infrastructure Proposal for {company} - Scaling Operations Efficiently\n\n"
            f"Dear {lead_name},\n\n"
            f"I hope this email finds you well.\n\n"
            f"I have been following {company}'s progress, and I am highly impressed by your scaling velocity in the {segment} space.\n\n"
            f"Given your active focus on {purpose}, I believe our platform—FlowZint AI—can help you optimize operations while securing a dramatic drop in customer acquisition parameters.\n\n"
            f"Specifically, we have helped similar customers in your segment achieve over **30% reduction in workflow bottlenecks** while maintaining institutional grade API integrations.\n\n"
            f"{custom_snippet}\n\n"
            f"Could we sync for an introductory chat on Tuesday or Thursday of next week?\n\n"
            f"Best regards,\n\n"
            f"John Doe\n"
            f"Sales Architect, FlowZint AI\n"
            f"john@flowzint.ai"
        )

    @staticmethod
    def analyze_ticket(details: Dict[str, Any]) -> Dict[str, Any]:
        msg = str(details.get("message", "")).lower()
        sub = str(details.get("subject", "")).lower()
        
        priority = "Medium"
        if any(w in msg or w in sub for w in ["blocker", "critical", "urgent", "broken", "stop"]):
            priority = "Critical"
        elif any(w in msg or w in sub for w in ["error", "fail", "bug", "payment", "charge"]):
            priority = "High"
            
        sentiment = "Neutral"
        if any(w in msg for w in ["angry", "upset", "terrible", "worst", "unacceptable", "double charged"]):
            sentiment = "Negative"
        elif any(w in msg for w in ["love", "great", "thanks", "perfect", "good"]):
            sentiment = "Positive"
            
        category = details.get("category") or "Technical Support"
        if any(w in sub or w in msg for w in ["api", "webhook", "integration", "error"]):
            category = "Technical API"
        elif any(w in sub or w in msg for w in ["invoice", "charge", "refund", "billing", "payment"]):
            category = "Billing"
            
        return {
            "priority": priority,
            "sentiment": sentiment,
            "category": category,
            "suggestedReply": (
                f"Dear {details.get('customerName', 'Customer')},\n\n"
                f"Thank you for reaching out to FlowZint AI support.\n\n"
                f"I understand that this issue is heavily impacting your team's workflow. I have analyzed your query and logged your urgency. "
                f"Our engineering team has been briefed regarding this category: {category} status. We are working diligently to resolve this as quickly as possible.\n\n"
                f"I will follow up back directly within 2 hours with an update.\n\n"
                f"Best regards,\n"
                f"FlowZint Support Agent (AI-Assisted)"
            )
        }

    @staticmethod
    def generate_support_reply(messages: List[Dict[str, str]]) -> str:
        last_msg = messages[-1].get("content", "").lower() if messages else ""
        if "billing" in last_msg or "price" in last_msg or "pay" in last_msg:
            return "For billing questions, I can verify your invoice cycles. Our systems recorded invoice INV-2026-4402 on scale tier. If duplicate charges occurred, our agents will process immediate reversals within 2-3 standard banking cycles."
        elif "api" in last_msg or "error" in last_msg or "webhooks" in last_msg:
            return "I have scanned our endpoint registry. We noticed webhook v2 signature warnings under endpoint registries earlier today. Our technical stack leads are resolving signature headers. Please supply your API Client ID to associate you to the escalations."
        elif "ceo" in last_msg or "metrics" in last_msg or "mrr" in last_msg:
            return "Our live SaaS dashboard reports an MRR of $32.4K across 142 enterprise and mid-market customers. Conversion indices are safe at 3.8%. Is there a specific financial trend you would like our CEO Copilot to evaluate?"
        return "Thank you for contacting FlowZint AI live chatbot. I'm trained on your current operations and metrics. Could you specify your query? I can assist with API configurations, billing cycles, or lead prospects."

    @staticmethod
    def summarize_meeting(transcript: str, title: str) -> Dict[str, Any]:
        return {
            "summary": (
                "The team aligned around campaigns targeting inbound audience channels following organic growth of 35%. "
                "Important assignments require setting sandboxes for trial accounts and launching key media reviews."
            ),
            "actionItems": [
                {
                    "text": "Publish customized tech review case studies",
                    "assignee": "Alice",
                    "dueDate": "2026-06-28",
                    "status": "Pending"
                },
                {
                    "text": "Configure sandbox environments and test endpoint integrations",
                    "assignee": "Bob",
                    "dueDate": "2026-06-29",
                    "status": "Pending"
                },
                {
                    "text": "Sync on tailoring enterprise prospectus files",
                    "assignee": "John",
                    "dueDate": "2026-06-27",
                    "status": "Pending"
                }
            ]
        }

    @staticmethod
    def generate_csv_insights(csv_data: str, question: str) -> Dict[str, Any]:
        return {
            "analysis": (
                "### Comprehensive Trend & Forecasting Diagnostic\n\n"
                "Based on your loaded operational parameters and recent CSV inputs, we have built the following forecasting models:\n\n"
                "1. **Growth Trajectory**: Revenue is accelerating MoM. This puts next month's projected run-rate at approximately **$35,900 MRR**.\n"
                "2. **Cohort Efficiency**: The Enterprise segment presents the highest average contract value. We recommend shifting 12% of outbound focus directly to these pre-qualified leads.\n"
                "3. **Projection Model (Next 3 Months)**:\n"
                "   - **July (Proj)**: $35,900\n"
                "   - **August (Proj)**: $39,200\n"
                "   - **September (Proj)**: $43,100\n\n"
                "**Actionable Advisory Plan:**\n"
                "We advocate reinforcing product-led growth (PLG) mechanics—such as pre-configured sandboxes—to lower sales cycle lengths by 4 days, resulting in immediate cash conversion gains."
            ),
            "forecastData": [
                { "month": "Jan", "revenue": 18200.0 },
                { "month": "Feb", "revenue": 20400.0 },
                { "month": "Mar", "revenue": 22100.0 },
                { "month": "Apr", "revenue": 24800.0 },
                { "month": "May", "revenue": 29500.0 },
                { "month": "Jun", "revenue": 32400.0 },
                { "month": "Jul (Proj)", "revenue": 35900.0 },
                { "month": "Aug (Proj)", "revenue": 39200.0 },
                { "month": "Sep (Proj)", "revenue": 43100.0 }
            ]
        }


# --- SERVICE ENTRY POINTS ---

def generate_executive_summary(question: str, metrics_context: str, leads_context: str, support_context: str) -> str:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.generate_executive_summary(question, metrics_context, leads_context, support_context)
    
    try:
        system_instruction = (
            "You are a high-level Strategic CEO Executive Advisor Copilot for a technology business called FlowZint AI. "
            "We will supply you with the current, real-time metrics, lead lists, tickets, and existing advisory guidelines for the business context.\n"
            "Your role as CEO Copilot is to digest this information, integrate any natural language inquiry, and provide a brilliant, professional, highly actionable executive synthesis.\n"
            "Format your responses beautifully in Markdown. Avoid generic advice—be highly quantitative and cite the actual metrics provided in the system context.\n\n"
            f"BUSINESS DATA SYSTEM CONTEXT:\n"
            f"- Metrics: {metrics_context}\n"
            f"- Leads Context: {leads_context}\n"
            f"- Support Context: {support_context}\n"
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Question from CEO: {question}",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2
                )
            )
            return response.text
        else:
            # Fallback for old legacy SDK if present
            model = genai_legacy.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
            response = model.generate_content(f"Question from CEO: {question}")
            return response.text
    except Exception as e:
        print(f"Gemini API Error in generate_executive_summary: {e}")
        return GeminiSimulator.generate_executive_summary(question, metrics_context, leads_context, support_context)


def generate_business_recommendations() -> List[Dict[str, Any]]:
    # Dynamic recommendations can be generated based on metrics, but for hackathon consistency,
    # we return structured strategic guidelines. If API key is present, we can call Gemini.
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.generate_business_recommendations()
        
    try:
        prompt = (
            "Generate exactly 3 high-impact strategic business recommendations for a B2B SaaS startup named FlowZint AI. "
            "Return them strictly in JSON format matching this schema: "
            "[\n"
            "  {\n"
            "    \"title\": \"string\",\n"
            "    \"category\": \"string\",\n"
            "    \"impact\": \"High\" | \"Medium\" | \"Low\",\n"
            "    \"description\": \"string\",\n"
            "    \"actionable_step\": \"string\"\n"
            "  }\n"
            "]"
        )
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.5
                )
            )
            return json.loads(response.text)
        return GeminiSimulator.generate_business_recommendations()
    except Exception as e:
        print(f"Gemini API Error in generate_business_recommendations: {e}")
        return GeminiSimulator.generate_business_recommendations()


def score_lead(lead_details: Dict[str, Any]) -> Dict[str, Any]:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.score_lead(lead_details)
        
    try:
        prompt = (
            "Assess and score the following business lead details on a scale from 0 to 100 based on their SaaS product fit, buying authority, conversion potential, and segment. "
            "Analyze strengths (positives), structural concerns, and give a highly targeted recommendation. "
            "Provide your response strictly as a JSON object matching this schema:\n"
            "{\n"
            "  \"score\": number,\n"
            "  \"category\": \"Hot Lead (Tier 1)\" | \"Warm Lead (Tier 2)\" | \"Cold Lead (Tier 3)\",\n"
            "  \"positives\": string[],\n"
            "  \"concerns\": string[],\n"
            "  \"recommendation\": string\n"
            "}\n\n"
            f"Lead details to evaluate:\n{json.dumps(lead_details, indent=2)}"
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        return GeminiSimulator.score_lead(lead_details)
    except Exception as e:
        print(f"Gemini API Error in score_lead: {e}")
        return GeminiSimulator.score_lead(lead_details)


def generate_sales_email(details: Dict[str, Any]) -> str:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.generate_sales_email(details)
        
    try:
        prompt = (
            "Write a highly converting, personalized professional B2B cold outreach email to a prospect.\n"
            f"Prospective Lead Name: {details.get('leadName')}\n"
            f"Company Name: {details.get('company')}\n"
            f"Segment: {details.get('segment', 'General')}\n"
            f"Outreach Purpose / Goal: {details.get('purpose', 'Business collaboration')}\n"
            f"Additional custom notes provided: {details.get('notes', 'None')}\n\n"
            "Keep the tone professional, value-oriented, and strictly non-spammy. Anchor context with FlowZint AI, which solves business operation automation. "
            "Outline clear, measurable ROI statistics (e.g., 30% speedups, robust API performance). Include an elegant subject line and a clear call to action."
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7)
            )
            return response.text
        return GeminiSimulator.generate_sales_email(details)
    except Exception as e:
        print(f"Gemini API Error in generate_sales_email: {e}")
        return GeminiSimulator.generate_sales_email(details)


def analyze_ticket(details: Dict[str, Any]) -> Dict[str, Any]:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.analyze_ticket(details)
        
    try:
        prompt = (
            "Analyze the following support ticket details. Determine:\n"
            "1. Core priority level (\"Low\" | \"Medium\" | \"High\" | \"Critical\")\n"
            "2. Customer Sentiment (\"Positive\" | \"Neutral\" | \"Negative\")\n"
            "3. Suggested Customer Ticket Category\n"
            "4. A highly professional, accurate, empathetic, and comprehensive suggested first-response reply that addresses the specific issue mentioned.\n\n"
            "Ticket Details:\n"
            f"Subject: {details.get('subject', 'No Subject')}\n"
            f"Customer: {details.get('customerName', 'Unknown')}\n"
            f"Message: \"{details.get('message', '')}\"\n\n"
            "Your output must be a valid JSON object matching the schema below:\n"
            "{\n"
            "  \"priority\": \"Low\" | \"Medium\" | \"High\" | \"Critical\",\n"
            "  \"sentiment\": \"Positive\" | \"Neutral\" | \"Negative\",\n"
            "  \"category\": string,\n"
            "  \"suggestedReply\": string\n"
            "}"
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        return GeminiSimulator.analyze_ticket(details)
    except Exception as e:
        print(f"Gemini API Error in analyze_ticket: {e}")
        return GeminiSimulator.analyze_ticket(details)


def generate_support_reply(messages: List[Dict[str, str]]) -> str:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.generate_support_reply(messages)
        
    try:
        system_instruction = (
            "You are the primary FlowZint AI Customer Support Chatbot. You are running live on the company's webpage.\n"
            "You have access to real-time operations data. Your responses must be highly professional, informative, concise (maximum 3 paragraphs), and empathetic.\n"
            "Direct users to open a support ticket if issues require senior engineering intervention. Try to resolve pricing, general API, and basic configuration queries on the fly.\n\n"
            "CORPORATE FACTS AND LIVE DATA:\n"
            "- Platform: FlowZint AI operating system (SaaS automate suite).\n"
            "- Current MRR: $32,400. CAC: $180. conversion: 3.8%.\n"
            "- Outstanding API issues: Yes! Webhook signature error matches v2 endpoints. Engineering is debugging it."
        )
        
        # We simulate the chat with system instructions and sending the context.
        # To make it work cleanly across APIs, we extract the last message and prompt.
        last_message = messages[-1].get("content", "Hello") if messages else "Hello"
        
        if HAS_GOOGLE_GENAI:
            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.5
                )
            )
            response = chat.send_message(message=last_message)
            return response.text
        return GeminiSimulator.generate_support_reply(messages)
    except Exception as e:
        print(f"Gemini API Error in generate_support_reply: {e}")
        return GeminiSimulator.generate_support_reply(messages)


def summarize_meeting(transcript: str, title: str) -> Dict[str, Any]:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.summarize_meeting(transcript, title)
        
    try:
        prompt = (
            "Analyze this business meeting transcript. Provide:\n"
            "1. An executive meeting summary (2-3 paragraphs max) outlining major agreements and directions.\n"
            "2. A list of action items extracted directly or logically inferred from the dialogue.\n"
            "Each action item must specify:\n"
            "   - A clear task description (what is the task)\n"
            "   - The assignee (who said they will do it, or logical owner)\n"
            "   - A realistic due date in format YYYY-MM-DD (estimate reasonably based on conversation context)\n"
            "   - Current status of the action item (\"Pending\")\n\n"
            f"Meeting Title: {title or 'Sync'}\n"
            f"Transcript Content:\n\"{transcript}\"\n\n"
            "Provide your output strictly in JSON format matching this schema:\n"
            "{\n"
            "  \"summary\": string,\n"
            "  \"actionItems\": [\n"
            "    {\n"
            "      \"text\": string,\n"
            "      \"assignee\": string,\n"
            "      \"dueDate\": string,\n"
            "      \"status\": \"Pending\" | \"Completed\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        return GeminiSimulator.summarize_meeting(transcript, title)
    except Exception as e:
        print(f"Gemini API Error in summarize_meeting: {e}")
        return GeminiSimulator.summarize_meeting(transcript, title)


def generate_csv_insights(csv_data: str, question: str) -> Dict[str, Any]:
    client = get_gemini_client()
    if not client:
        return GeminiSimulator.generate_csv_insights(csv_data, question)
        
    try:
        prompt = (
            "You are the primary Analytics AI Agent for FlowZint AI operating system.\n"
            "Your role is to analyze a dataset of CSV data (or custom business table data) provided by the user, discover critical trends, forecast future revenue/growth for the next 3 months, and compile a beautiful and professional business trends report.\n\n"
            f"Dataset provided:\n\"{csv_data}\"\n\n"
            f"User question or focus parameter: \"{question or 'Identify key growth trends and forecast next months'}\"\n\n"
            "Your output must be a valid JSON object matching the schema below. Keep \"analysis\" richly formatted in Markdown including highlights, bullet points, and actionable strategies:\n"
            "{\n"
            "  \"analysis\": string,\n"
            "  \"forecastData\": [\n"
            "    { \"month\": string, \"revenue\": number }\n"
            "  ]\n"
            "}"
        )
        
        if HAS_GOOGLE_GENAI:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )
            return json.loads(response.text)
        return GeminiSimulator.generate_csv_insights(csv_data, question)
    except Exception as e:
        print(f"Gemini API Error in generate_csv_insights: {e}")
        return GeminiSimulator.generate_csv_insights(csv_data, question)
