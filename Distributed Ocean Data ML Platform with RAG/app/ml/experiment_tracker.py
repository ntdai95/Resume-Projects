import mlflow
from app.core.settings import settings


def log_run(run_name, params, metrics, experiment_name=None):
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(experiment_name or settings.mlflow_experiment_name)
    with mlflow.start_run(run_name=run_name):
        if params:
            mlflow.log_params(params)
            
        if metrics:
            mlflow.log_metrics(metrics)