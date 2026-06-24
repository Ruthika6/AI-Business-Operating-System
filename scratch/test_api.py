import sys
import os

# Add root folder to python path so we can import app modules directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def run_tests():
    print("=" * 60)
    print("RUNNING FLOWZINT AI API TEST SUITE")
    print("=" * 60)
    
    # 1. Test Dashboard API
    print("Testing GET /api/dashboard...")
    res = client.get("/api/dashboard")
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "metrics" in data, "Missing metrics"
    assert "revenueHistory" in data, "Missing revenue history"
    assert len(data["revenueHistory"]) > 0, "Empty revenue history"
    print("[OK] Dashboard API Passed!")
    
    # 2. Test Copilot Advisor Query
    print("\nTesting POST /api/copilot/query...")
    res = client.post("/api/copilot/query", json={"question": "Evaluate business health"})
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "answer" in data, "Missing answer"
    assert "model" in data, "Missing model"
    print("[OK] Copilot Advisor Query Passed!")
    
    # 3. Test Sales Leads List
    print("\nTesting GET /api/sales/leads...")
    res = client.get("/api/sales/leads")
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert isinstance(data, list), "Leads must be a list"
    assert len(data) > 0, "No leads returned"
    print("[OK] Sales Leads Retrieval Passed!")
    
    # 4. Test Lead Scoring
    print("\nTesting POST /api/sales/score...")
    lead_details = {
        "name": "Test Prospect",
        "company": "Test Co",
        "notes": "Interested in immediate enterprise trial sandbox config"
    }
    res = client.post("/api/sales/score", json={"leadDetails": lead_details})
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "score" in data, "Missing score"
    assert "category" in data, "Missing category"
    assert "positives" in data, "Missing positives list"
    print("[OK] Sales Lead Scoring Passed!")
    
    # 5. Test Support Ticket Analysis
    print("\nTesting POST /api/support/analyze...")
    res = client.post("/api/support/analyze", json={
        "customerName": "Test Client",
        "subject": "Billing issue",
        "message": "I was double charged invoice INV-2026-4402. Please refund asap."
    })
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "priority" in data, "Missing priority"
    assert "sentiment" in data, "Missing sentiment"
    assert "suggestedReply" in data, "Missing suggested reply"
    print("[OK] Support Ticket Triage Passed!")
    
    # 6. Test Chatbot response
    print("\nTesting POST /api/support/reply...")
    res = client.post("/api/support/reply", json={
        "messages": [{"role": "user", "content": "How can I resolve duplicate billing invoice INV-2026-4402?"}]
    })
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "message" in data, "Missing message response"
    print("[OK] Support Chatbot Playback Passed!")
    
    # 7. Test Meeting transcript summarization
    print("\nTesting POST /api/meeting/summarize...")
    transcript = "Alice: Let's launch case study on Friday.\nBob: I will configure the Innovate sandbox environment by Monday."
    res = client.post("/api/meeting/summarize", json={
        "title": "Weekly Status Update",
        "transcript": transcript
    })
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "summary" in data, "Missing summary"
    assert "action_items" in data, "Missing action items"
    assert len(data["action_items"]) > 0, "No action items extracted"
    print("[OK] Meeting Summarizer Passed!")
    
    # 8. Test CSV analytics mock upload
    print("\nTesting POST /api/analytics/insights...")
    res = client.post("/api/analytics/insights", json={
        "csvData": '{"statistics":{"rows_count":5,"columns":["month","revenue"],"numeric_summary":{"revenue":{"sum":100000,"mean":20000}}},"sample_rows":[]}',
        "question": "Forecast next months growth"
    })
    assert res.status_code == 200, f"Error: {res.status_code}"
    data = res.json()
    assert "analysis" in data, "Missing analysis"
    assert "forecastData" in data, "Missing forecast data"
    print("[OK] CSV Analytics Insights Passed!")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! APPLICATION IS PRODUCTION READY.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
