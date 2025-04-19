from typing import TYPE_CHECKING

import mlflow

if TYPE_CHECKING:
    from databricks.agents.review_app import ReviewApp


def get_review_app_v2_from_model_version(
    model_name: str, model_version: str, endpoint_name: str
) -> "ReviewApp":
    from databricks.agents.review_app import get_review_app

    client = mlflow.MlflowClient()
    model_info = client.get_model_version(model_name, model_version)
    experiment_id = client.get_run(model_info.run_id).info.experiment_id
    # This is idempotent, acts as get_or_create.
    review_app_v2 = get_review_app(experiment_id)
    # This is idempotent as long as the agent_name and model_serving_endpoint are stable.
    review_app_v2.add_agent(
        agent_name=model_name,
        model_serving_endpoint=endpoint_name,
    )
    return review_app_v2


def get_review_app_v2_url(review_app_v2: "ReviewApp") -> str:
    return review_app_v2.url + "/chat"
