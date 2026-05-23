from locust import HttpUser, task, between
import random

class ChurnUser(HttpUser):

    wait_time = between(1, 3)



    @task
    def predict_churn(self):
        # Use the same payload structure as your ChurnRequest model
        payload = {
            "CreditScore": random.randint(350, 850),
            "Geography": random.choice(["France", "Germany", "Spain"]),
            "Gender": random.choice(["Male", "Female"]),
            "Age": random.randint(18, 90),
            "Tenure": random.randint(0, 10),
            "Balance": round(random.uniform(0, 250000), 2),
            "NumOfProducts": random.randint(1, 4),
            "HasCrCard": random.choice([0, 1]),
            "IsActiveMember": random.choice([0, 1]),
            "EstimatedSalary": round(random.uniform(0, 200000), 2),
        }

        # POST to the /predict endpoint
        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                # optional: verify response structure
                if "prediction" not in data or "label" not in data:
                    response.failure("Missing prediction or label in response")
            else:
                response.failure(f"Unexpected status code: {response.status_code}")

    # Optional: ping health endpoint occasionally (not necessary)
    @task(1)  # lower weight: 1 out of e.g. 11 tasks (if you add more)
    def health_check(self):
        self.client.get("/health")