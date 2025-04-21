import mlflow
from fairops.mlops.autolog import LoggerFactory
import random


mlflow.set_experiment("autolog_example")

ml_logger = LoggerFactory.get_logger("mlflow")

with mlflow.start_run() as parent_run:
    mlflow.log_param("n_trials", 2)
    for i in range(0, 2):
        with mlflow.start_run(nested=True) as run:
            mlflow.log_param("loss", 0.001)
            mlflow.log_params({
                "beta_1": 0.001,
                "model_type": "nn",
                "idx": i
            })

            for step in range(5):
                mlflow.log_metric("accuracy", round(random.uniform(0.0, 0.99), 2), step=step)

            test_metrics = {
                "test_accuracy": round(random.uniform(0.0, 0.99), 2),
                "test_specificity": round(random.uniform(0.0, 0.99), 2)
            }

            mlflow.log_metrics(test_metrics)
            ml_logger.export_logs_as_artifact()
            mlflow.end_run()

    ml_logger.export_logs_as_artifact()
    mlflow.end_run()
