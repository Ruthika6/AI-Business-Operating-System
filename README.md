 AI Business Operating System

AI-powered Business Operating System built specifically for the FlowZint AI Hackathon (Open Innovation Category). 

This platform serves as a centralized control center for startups and enterprises, using Google Gemini to automate business strategy, sales CRM activities, customer support triaging, meeting minutes summarization, and CSV data analytics.

---

## 🎨 Creative Architecture & Visual System

FlowZint AI is designed with a premium, high-fidelity **glassmorphism user interface** showcasing a dark twilight corporate control panel, custom line/bar charts, glowing state signals, and animations.

- **CEO Advisor**: Tracks financial SaaS metrics (MRR, LTV, CAC), displays revenue trends, offers strategic recommendations, and features an interactive CEO Copilot strategic Q&A chat powered by Gemini.
- **Sales AI Agent**: Implements inbound lead management, scores leads with detailed pros/cons evaluations, and personalizes structured B2B cold email proposals.
- **Support AI Agent**: Triages helpdesk tickets by detecting priority and customer sentiment, drafts empathetic suggested replies, and features a live chat simulator playground.
- **Meeting Minutes**: Ingests call transcripts, outputs executive summaries, and extracts action items with assignees and logical deadlines into a checklist.
- **CSV Analytics**: Automates cleaning of custom datasets, computes descriptive statistics using Pandas/NumPy, projects 3-month growth forecasts, and renders detailed analysis dossiers.

---

## 📂 Project Directory Structure

```text
ai-business-operating-system/
├── app.py                # Main FastAPI instantiator & database seeder
├── config.py             # App environment variables & dynamic DB path mapper
├── database.py           # SQLAlchemy engine & session pool manager
├── models.py             # SQLAlchemy models (User, Lead, SupportTicket, etc.)
├── schemas.py            # Pydantic validation schemas
├── vercel.json           # Vercel Serverless routing configuration
├── requirements.txt      # Python dependencies list
├── Dockerfile            # Container definition
├── render.yaml           # Render deployment template
├── .env.example          # Environment variables template
├── routers/              # Modular endpoint files
│   ├── dashboard.py      # CEO advisor APIs & Q&A
│   ├── sales.py          # CRM pipeline & email personalization
│   ├── support.py        # Tickets triaging & chatbot simulator
│   ├── meeting.py        # Transcripts summarizer & task checklist
│   └── analytics.py      # CSV uploads & trend analysis
├── services/             # Intelligent business service logic
│   ├── gemini_service.py # Gemini SDK integrations & mock fallbacks
│   ├── sales_service.py  # CRM database logic
│   ├── support_service.py# Ticketing database logic
│   ├── meeting_service.py# Transcript summarizer logic
│   └── analytics_service.py # Pandas dataset cleaning & statistics
├── templates/            # HTML5 Jinja2 UI Templates
│   ├── base.html         # Sidebar framework, styling & icons
│   ├── dashboard.html    # CEO charts & copilot widget
│   ├── sales.html        # CRM datagrid & outreach composer
│   ├── support.html      # Tickets board & chatbot playground
│   ├── meetings.html     # Meetings archives & checklist
│   └── analytics.html    # CSV processor & forecasting chart
└── static/               # Static Assets
    ├── css/
    │   └── style.css     # Dark mode theme & glassmorphic layouts
    └── js/
        └── main.js       # Toast notices & api wrappers
```

---

## 🚀 Local Development Setup

To run FlowZint AI locally, follow these steps:

### 1. Prerequisite Requirements
- Python 3.11+
- Pip (Python Package Manager)
- A **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/) (Optional: The application runs a robust simulation mode out-of-the-box if no API key is specified).

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Secrets
Copy the environment template and insert your Gemini API Key:
```bash
cp .env.example .env
```
Open `.env` and fill in:
```env
GEMINI_API_KEY="your-actual-api-key-here"
```

### 4. Run Application
Start the FastAPI server via Uvicorn:
```bash
uvicorn app:app --reload --port 8000
```
Open your browser and navigate to `http://localhost:8000`. The database will automatically initialize and seed with default metrics so you can test features immediately.

---

## 🌍 Vercel Deployment Guide

FlowZint AI is designed to deploy on Vercel as a stateless Python serverless application.

### Step 1: Push Code to GitHub
Ensure all application files are in the root of your GitHub repository.

### Step 2: Import Project to Vercel
1. Go to the [Vercel Dashboard](https://vercel.com/) and click **Add New > Project**.
2. Select your GitHub repository.

### Step 3: Configure Environment Variables
In the **Environment Variables** section of the Vercel project setup, add:
- `GEMINI_API_KEY`: Your Gemini API Key from Google AI Studio.
- `DATABASE_URL`: (Optional) Supply a PostgreSQL connection string (e.g., from Neon or Supabase) to enable persistent data writes. If not supplied, the app will run using a stateless SQLite database file located in `/tmp/flowzint.db` (data will reset when the serverless function cold-starts).

### Step 4: Deploy
Click **Deploy**. Vercel will detect `vercel.json` and build the application using the `@vercel/python` engine. Once complete, your project will be live!

---

## 🐋 Docker & Alternative Deployments

### Docker Build
To compile a Docker container:
```bash
docker build -t flowzint-ai .
docker run -p 8000:8000 -e GEMINI_API_KEY="your_api_key" flowzint-ai
```

### Render Deployment
Use the button on Render or connect your repository. Render will automatically detect the `render.yaml` configuration and launch the service.
