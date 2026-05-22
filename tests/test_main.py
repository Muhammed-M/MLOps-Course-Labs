"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""

from litestar.testing import TestClient

from app.model_utils import predict_churn
from main import app

VALID_FEATURES = [619, "France", "Female", 42, 2, 0.0, 1, 1, 1, 101348.88]

VALID_PAYLOAD = {
    "CreditScore": 619,
    "Geography": "France",
    "Gender": "Female",
    "Age": 42,
    "Tenure": 2,
    "Balance": 0.0,
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": 101348.88,
}

INVALID_PAYLOAD = {
    "CreditScore": "619",
    "Geography": 986,
    "Gender": 4352627,
    "Age": "France",
    "Tenure": 2,
    "Balance": "France",
    "NumOfProducts": 1,
    "HasCrCard": 1,
    "IsActiveMember": 1,
    "EstimatedSalary": "Germany",
}



# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------

# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
#         Hint: import predict_churn from app.model_utils

def test_predict_churn_returns_binary():
    result = predict_churn(VALID_FEATURES)
    assert result in (0, 1), f"Expected 0 or 1, got {result}"



# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_edge_case():
    edge_features = [0, "Germany", "Male", 100, 10, 999999.0, 4, 0, 0, 0.0]
    result = predict_churn(edge_features)
    assert result in (0, 1), f"Expected 0 or 1, got {result}"





# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------

# TODO 3: Write a test that POSTs to /predict with valid JSON
#         and checks the status code and response body
#         Hint: Litestar POST returns 201, not 200
#         Hint: use `with TestClient(app=app) as client:`

def test_predict_endpoint():
    with TestClient(app=app) as client:
        response = client.post("/predict", json=VALID_PAYLOAD)

    assert response.status_code == 200           # POST = 200 , i edited it 
    body = response.json()
    assert "prediction" in body
    assert body["prediction"] in (0, 1)
    assert "label" in body
    assert body["label"] in ("Churn", "No Churn")



# TODO 4: Write a test for GET /health

def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# TODO 5: Write a test for GET /

def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# TODO 6 (bonus): Test that invalid input returns status 400

def test_predict_invalid_input_returns_400():
    with TestClient(app=app) as client:
        response = client.post("/predict", json=INVALID_PAYLOAD)
    assert response.status_code == 400
