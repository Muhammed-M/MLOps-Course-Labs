"""
Model loading and prediction logic.

The model must be loaded ONCE at module level, NOT inside the predict function.
"""
import joblib
import pandas as pd

model = joblib.load("data/pipeline.joblib")

FEATURE_NAMES = [
    "CreditScore", "Geography", "Gender", "Age", "Tenure",
    "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary",
]



def predict_churn(features: list[float]) -> int:
    """
    Takes a list of feature values and returns a churn prediction (0 or 1).
    """
    # TODO 2: Use model.predict() to get a prediction and return it as an int
    #         Hint: model.predict() expects a 2D array

    df = pd.DataFrame([features], columns=FEATURE_NAMES)
    prediction = model.predict(df.values)
    return int(prediction[0])




if __name__ == "__main__":
    # TODO 3: Replace with sample features that match your model
    sample = [619, "France", "Male", 42, 2, 0.0, 1, 1, 1, 101348.88]
    print(f"Input:      {sample}")
    print(f"Prediction: {predict_churn(sample)}")
