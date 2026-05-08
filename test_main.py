from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sync_and_get_user():
    payload = {
        "user_id": "test_user_123",
        "user": {
            "name": "Test",
            "gender": "nam",
            "age": 25,
            "weight": 70.0,
            "height": 175.0,
            "bmi": 22.8,
            "goal": "giam_can",
            "activity": "vua",
            "createdAt": "2023-10-01T00:00:00Z"
        },
        "tracking": [
            {"date": "2023-10-01T00:00:00Z", "meals_done": True, "weight": 70.0}
        ]
    }
    
    # 1. Sync
    response = client.post("/api/sync", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    
    # 2. Get User
    response = client.get("/api/user/test_user_123")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["name"] == "Test"
    assert len(data["tracking"]) == 1
    
    # 3. Get Leads
    response = client.get("/api/admin/leads")
    assert response.status_code == 200
    leads = response.json()
    assert len(leads) >= 1
    assert any(l["user_id"] == "test_user_123" for l in leads)
