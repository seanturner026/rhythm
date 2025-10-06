import logging
import os

import mlflow
from mlflow.exceptions import MlflowException
from mlflow.sklearn import log_model
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

MODEL_NAME = "sk-learn-random-forest-reg-model"
EXPERIMENT_NAME = "random-forest-regression"


def get_mlflow_client():
    """
    Get MLflow client with proper tracking URI
    """
    mlflow_host = os.getenv("MLFLOW_HOST", "localhost")
    mlflow_port = os.getenv("MLFLOW_PORT", "5000")
    mlflow_uri = f"http://{mlflow_host}:{mlflow_port}"
    mlflow.set_tracking_uri(mlflow_uri)
    return mlflow.MlflowClient()


def get_or_create_experiment():
    """
    Get existing experiment or create a new one
    """
    try:
        experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
        if experiment is None:
            logger.info(f"Creating experiment '{EXPERIMENT_NAME}'")
            experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
        else:
            experiment_id = experiment.experiment_id
        logger.info(f"Using experiment '{EXPERIMENT_NAME}' (ID: {experiment_id})")
        return experiment_id
    except Exception as e:
        logger.warning(f"Error getting/creating experiment: {e}, using default")
        return "0"


def train_and_register_model():
    """
    Train a new model and register it in MLflow
    """
    logger.info("Training regression model...")

    experiment_id = get_or_create_experiment()

    with mlflow.start_run(experiment_id=experiment_id):
        X, y = make_regression(n_features=4, n_informative=2, random_state=0, shuffle=False)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        params = {"max_depth": 2, "random_state": 42}
        model = RandomForestRegressor(**params)
        model.fit(X_train, y_train)
        _ = mlflow.log_params(params)

        y_pred = model.predict(X_test)
        _ = mlflow.log_metrics({"mse": mean_squared_error(y_test, y_pred)})

        _ = log_model(
            sk_model=model,
            artifact_path="model",
            input_example=X_train,
            registered_model_name=MODEL_NAME,
        )

    logger.info(f"Model '{MODEL_NAME}' trained and registered successfully")


def ensure_model_exists():
    """Check if model exists, train and register if it doesn't"""
    client = get_mlflow_client()

    try:
        _ = client.get_registered_model(MODEL_NAME)
        logger.info(f"Model '{MODEL_NAME}' already exists")
    except MlflowException:
        logger.info(f"Model '{MODEL_NAME}' not found, training new model...")
        train_and_register_model()
