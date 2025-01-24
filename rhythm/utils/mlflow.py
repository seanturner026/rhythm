import os

import mlflow


def configure_mlflow():
    """
    Configures mlflow. If the environment is docker compose environment variables are used to accommodate the different
    host and port (connection by service name and port rather than localhost and host port).
    """
    MLFLOW_HOST: str = os.getenv("MLFLOW_HOST", "localhost")
    MLFLOW_PORT: str = os.getenv("MLFLOW_PORT", str(3000))
    mlflow.set_tracking_uri(f"http://{MLFLOW_HOST}:{MLFLOW_PORT}")
