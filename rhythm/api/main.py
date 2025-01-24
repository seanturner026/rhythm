import logging
from enum import Enum

import mlflow
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

from rhythm.utils.mlflow import configure_mlflow

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
app = FastAPI()

configure_mlflow()


model_uri: str = "models:/tracking-quickstart/1"
model = mlflow.sklearn.load_model(model_uri=model_uri)
logger.info("server ready")


class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class IrisSpecies(Enum):
    SETOSA = 0
    VERSICOLOR = 1
    VIRGINICA = 2


@app.post("/predict")
async def predict(request: IrisRequest):
    features = np.array(
        [
            [request.sepal_length, request.sepal_width, request.petal_length, request.petal_width],
        ]
    )
    prediction = model.predict(features)[0]
    return {"prediction": IrisSpecies(prediction).name.lower()}


# S3_BUCKET_NAME: str = ""
# client = boto3.client("s3")
#
#
# class PredictionRequest(BaseModel):
#     input_dataset_path: str
#
#
# @app.get("/predict")
# def get_predict(request: PredictionRequest, client):
#     s3_response = client.get_object(Bucket=S3_BUCKET_NAME, Key=request.input_dataset_path)
#     dataset = s3_response.Body
#
#     predictions = model.predict(pd.read_csv(dataset))
#     predictions.to_csv("output.csv")
#
#     return {"Hello": "World"}
