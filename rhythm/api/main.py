import logging
import os

import mlflow
import numpy as np
from fastapi import FastAPI
from mlflow.sklearn import load_model
from pydantic import BaseModel

from rhythm.pipelines.train import MODEL_NAME, ensure_model_exists

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI()

logger.info("Server initializing...")
mlflow_host = os.getenv("MLFLOW_HOST", "localhost")
mlflow_port = os.getenv("MLFLOW_PORT", "5000")
mlflow_uri = f"http://{mlflow_host}:{mlflow_port}"
mlflow.set_tracking_uri(mlflow_uri)
logger.info(f"Connecting to MLflow at {mlflow_uri}")

ensure_model_exists()

model_uri = f"models:/{MODEL_NAME}/latest"
model = load_model(model_uri=model_uri)
logger.info("Server ready")


class PredictionRequest(BaseModel):
    feature_1: float
    feature_2: float
    feature_3: float
    feature_4: float


@app.post("/predict")
async def predict(request: PredictionRequest):
    features = np.array(
        [
            [request.feature_1, request.feature_2, request.feature_3, request.feature_4],
        ]
    )
    prediction = model.predict(features)[0]
    return {"prediction": float(prediction)}
