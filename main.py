"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar, get, post
from pydantic import BaseModel

from app.logger_setup import setup_logging
from app.model_utils import FEATURE_NAMES, predict_churn

logger = setup_logging()


# ---------------------------------------------------------------------------
# Request Schema
# ---------------------------------------------------------------------------

    # filter_feat = [
    #     "CreditScore",
    #     "Geography",
    #     "Gender",
    #     "Age",
    #     "Tenure",
    #     "Balance",
    #     "NumOfProducts",
    #     "HasCrCard",
    #     "IsActiveMember",
    #     "EstimatedSalary",
    # ]


class ChurnRequest(BaseModel):

    CreditScore: float
    Geography: str
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float


class ChurnResponse(BaseModel):
    prediction: int
    label: str
    message: str = "Prediction successful" 


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

# TODO 2: Create a GET endpoint at "/" that returns a welcome message
#         Log that the home endpoint was accessed

@get("/")
async def home() -> dict:
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to the Churn Prediction API"}



# TODO 3: Create a GET endpoint at "/health" that returns {"status": "healthy"}

@get("/health")
async def health() -> dict:
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

# TODO 4: Create a POST endpoint at "/predict" that:
#         - Accepts a ChurnRequest as the data parameter
#         - Extracts features into a list
#         - Calls predict_churn(features)
#         - Returns the prediction
#         - Logs the input features and the prediction result


@post("/predict" , status_code=200)
async def predict(data: ChurnRequest) -> ChurnResponse:
    features = [
        data.CreditScore,
        data.Geography,
        data.Gender,
        data.Age,
        data.Tenure,
        data.Balance,
        data.NumOfProducts,
        data.HasCrCard,
        data.IsActiveMember,
        data.EstimatedSalary,
    ]
    logger.info(f"Prediction request received | features: {features}")

    result = predict_churn(features)
    label = "Churn" if result == 1 else "No Churn"

    logger.info(f"Prediction result: {result} ({label})")
    return ChurnResponse(prediction=result, label=label , message="Prediction completed successfully")



# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
# TODO 5: Register your endpoint functions in the list below
app = Litestar(
    route_handlers=[home, health, predict],
)
