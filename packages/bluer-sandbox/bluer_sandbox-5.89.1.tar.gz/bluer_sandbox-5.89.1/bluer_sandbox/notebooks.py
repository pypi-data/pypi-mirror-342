import os

from bluer_objects import storage, mlflow

os.environ["MLFLOW_TRACKING_URI"] = os.path.join(
    os.environ.get("HOME"),
    "mlflow",
)


def upload(object_name: str) -> bool:
    return storage.upload(object_name) and mlflow.log_run(object_name)
