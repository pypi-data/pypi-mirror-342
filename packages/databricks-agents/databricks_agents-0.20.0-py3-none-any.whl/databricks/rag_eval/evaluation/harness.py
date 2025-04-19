"""Entry point to the evaluation harness"""

from __future__ import annotations

import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partialmethod
from typing import Dict, List, Optional, Union

import mlflow
import mlflow.tracing.constant as tracing_constant
from mlflow import entities as mlflow_entities
from mlflow.entities import assessment as mlflow_assessment
from mlflow.entities.assessment_error import AssessmentError
from mlflow.entities.assessment_source import AssessmentSource
from mlflow.tracing import fluent
from mlflow.utils.proto_json_utils import parse_pb_value
from tqdm.auto import tqdm

from databricks.rag_eval import context, env_vars, schemas, session
from databricks.rag_eval.clients.managedrag import managed_rag_client
from databricks.rag_eval.config import assessment_config, evaluation_config
from databricks.rag_eval.evaluation import (
    assessments,
    datasets,
    entities,
    metrics,
    models,
    per_run_metrics,
    rca,
    traces,
)
from databricks.rag_eval.evaluation import custom_metrics as agent_custom_metrics
from databricks.rag_eval.utils import input_output_utils, rate_limit

_logger = logging.getLogger(__name__)
_FAIL_TO_GET_TRACE_WARNING_MSG = re.compile(
    r"Failed to get trace from the tracking store"
)

EvalResults = List[entities.EvalResult]


# TODO(ML-52269): This is a temporary monkey patch to fix a pickling issue with `Trace.to_json`. It
# should be removed once we pin MLflow to 2.22.0 or later.
def patched_mlflow_assessment_from_proto(cls, proto):
    if proto.WhichOneof("value") == "expectation":
        expectation = mlflow_assessment.Expectation(
            parse_pb_value(proto.expectation.value)
        )
        feedback = None
    elif proto.WhichOneof("value") == "feedback":
        expectation = None
        feedback = mlflow_assessment.Feedback(parse_pb_value(proto.feedback.value))
    else:
        expectation = None
        feedback = None

    error = AssessmentError.from_proto(proto.error) if proto.error.error_code else None
    # This line contains the fix to allow `mlflow.get_trace(...).to_json()`
    metadata = dict(proto.metadata) if proto.metadata else None

    return cls(
        _assessment_id=proto.assessment_id or None,
        trace_id=proto.trace_id,
        name=proto.assessment_name,
        source=AssessmentSource.from_proto(proto.source),
        create_time_ms=proto.create_time.ToMilliseconds(),
        last_update_time_ms=proto.last_update_time.ToMilliseconds(),
        expectation=expectation,
        feedback=feedback,
        rationale=proto.rationale or None,
        metadata=metadata,
        error=error,
        span_id=proto.span_id or None,
    )


mlflow_entities.Assessment.from_proto = classmethod(
    patched_mlflow_assessment_from_proto
)


def run(
    *,
    eval_dataset: Union[datasets.EvaluationDataframe, List[entities.EvalItem]],
    config: evaluation_config.GlobalEvaluationConfig,
    experiment_id: Optional[str] = None,
    run_id: Optional[str] = None,
    model=None,
) -> EvalResults:
    """
    Run the logic of the eval harness.

    :param eval_dataset: The evaluation dataset
    :param config: The evaluation config
    :param experiment_id: The MLflow experiment ID to log the results to (used for logging traces)
    :param run_id: The MLflow run ID to log the results to (used for logging traces)
    :param model: Optional model to use for generating responses and traces
    """

    eval_items = (
        eval_dataset.eval_items
        if isinstance(eval_dataset, datasets.EvaluationDataframe)
        else eval_dataset
    )

    # Disable tqdm progress bar by default so that the progress bars inside MLflow eval_fn do not show
    tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)

    client = context.get_context().build_managed_rag_client()
    rate_limiter = _build_rate_limiter_for_assessment()

    # Emit usage events prior to all logic
    _emit_custom_assessments_usage_event_if_present(
        client, config.global_assessment_configs
    )

    eval_results = []
    with ThreadPoolExecutor(
        max_workers=env_vars.RAG_EVAL_MAX_WORKERS.get()
    ) as executor:
        futures = [
            executor.submit(
                _run_single,
                eval_item=eval_item,
                config=config.get_eval_item_eval_config(eval_item.question_id),
                model=model,
                client=client,
                rate_limiter=rate_limiter,
                current_session=session.current_session(),
                experiment_id=experiment_id,
                run_id=run_id,
            )
            for eval_item in eval_items
        ]

        futures_as_completed = as_completed(futures)
        # Add a progress bar to show the progress of the assessments
        futures_as_completed = tqdm(
            futures_as_completed,
            total=len(futures),
            disable=False,
            desc="Evaluating",
            smoothing=0,  # 0 means using average speed for remaining time estimates
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [Elapsed: {elapsed}, Remaining: {remaining}]",
        )

        for future in futures_as_completed:
            result = future.result()
            eval_results.append(result)

    # Compute aggregate metrics if there are custom metrics configured
    aggregate_metrics = None
    if config.custom_metrics:
        try:
            aggregate_metrics = per_run_metrics.compute_aggregate_metric_results(
                eval_results
            )
        except Exception as e:
            _logger.error(
                "Failed to compute aggregate metrics. Skipping emitting custom metric usage event.",
                exc_info=e,
            )

    _emit_custom_metric_usage_event_if_present(
        client, config.custom_metrics, metric_stats=aggregate_metrics
    )

    return eval_results


def _run_single(
    eval_item: entities.EvalItem,
    config: evaluation_config.ItemEvaluationConfig,
    client: managed_rag_client.ManagedRagClient,
    rate_limiter: rate_limit.RateLimiter,
    experiment_id: Optional[str] = None,
    run_id: Optional[str] = None,
    model: Optional[mlflow.pyfunc.PyFuncModel] = None,
    current_session: Optional[session.Session] = None,
) -> entities.EvalResult:
    """
    Run the logic of the eval harness for a single eval item.

    :param eval_item: The eval item to evaluate
    :param config: The evaluation config
    :param model: Optional model to use for generating responses and traces
    """
    session.set_session(current_session)
    # Do a best effort attempt to not copy the trace if it is from the same run
    # This metadata is added by us when we log the trace, so it is not guaranteed to be present
    is_trace_from_same_run = (
        eval_item.trace is not None
        # This is only present in V3 traces
        and hasattr(eval_item.trace.info, "metadata")
        and eval_item.trace.info.metadata[schemas.TRACE_METADATA_RUN_ID] == run_id
    )

    if model:
        eval_item = _populate_model_result_to_eval_item(
            eval_item=eval_item,
            model_result=models.invoke_model(model, eval_item, run_id),
        )
    elif eval_item.trace is not None:
        # If logging to MLflow is disabled, we don't need to clone the trace
        if (
            env_vars.AGENT_EVAL_LOG_TRACES_TO_MLFLOW_ENABLED.get()
            and not is_trace_from_same_run
        ):
            prepared_trace = traces.clone_trace_to_reupload(eval_item.trace)
            cloned_trace = traces.inject_experiment_run_id_to_trace(
                prepared_trace, experiment_id, run_id
            )
            eval_item.trace = cloned_trace
        eval_item = _populate_eval_item_with_trace(eval_item)
    else:
        minimal_trace = _create_minimal_trace(experiment_id, run_id, eval_item)
        eval_item.trace = minimal_trace
        eval_item = _populate_eval_item_with_trace(eval_item)

    # Skip the evaluation if invoking the model failed
    if eval_item.model_error_message is not None:
        try:
            client.emit_client_error_usage_event(eval_item.model_error_message)
        except Exception:
            # Telemetry logging failures are non-fatal.
            pass

        eval_result = _no_op_eval_result(eval_item)
    else:
        assessment_results = assessments.generate_llm_assessments(
            client=client,
            rate_limiter=rate_limiter,
            eval_item=eval_item,
            config=config,
        )

        metric_results = metrics.compute_eval_metrics(
            eval_item=eval_item,
            assessment_results=assessment_results,
            metrics=metrics.BUILT_IN_METRICS + config.custom_metrics,
        )

        eval_result = entities.EvalResult(
            eval_item=eval_item,
            assessment_results=assessment_results,
            overall_assessment=rca.compute_overall_assessment(
                assessment_results, metric_results
            ),
            metric_results=metric_results,
        )

    try:
        logged_trace = log_traces_and_assessments(
            experiment_id, run_id, eval_item.trace, eval_result.assessments
        )
        eval_result.eval_item.trace = logged_trace
    except Exception as e:
        # Failures in logging to MLflow should not fail the entire harness run
        _logger.warning(f"Failed to log trace and assessments to MLflow: {e}")

    return eval_result


def _no_op_eval_result(eval_item: entities.EvalItem) -> entities.EvalResult:
    """
    Create a no-op eval result for the eval item for skipping the evaluation.

    :param eval_item: The eval item to create a no-op eval result for
    :return: The no-op eval result
    """
    return entities.EvalResult(
        eval_item=eval_item,
    )


def _populate_model_result_to_eval_item(
    eval_item: entities.EvalItem, model_result: models.ModelResult
) -> entities.EvalItem:
    """
    Populate the model result to the eval item in place.

    :param eval_item: The eval item to populate the model result
    :param model_result: The model result to populate
    :return: The populated eval item
    """
    eval_item.answer = model_result.response
    # The response needs to be json-serializable, so we try to convert it to a dict.
    try:
        eval_item.raw_response = input_output_utils.parse_variant_data(
            model_result.raw_model_output
        )
    except Exception as e:
        raise ValueError(
            f"The response from the model must be JSON serializable: {type(model_result.raw_model_output)}. "
        ) from e
    eval_item.retrieval_context = model_result.retrieval_context
    eval_item.tool_calls = model_result.tool_calls
    eval_item.trace = model_result.trace
    eval_item.model_error_message = model_result.error_message
    return eval_item


def _create_minimal_trace(
    experiment_id: Optional[str], run_id: Optional[str], eval_item: entities.EvalItem
) -> mlflow_entities.Trace:
    trace = traces.create_minimal_trace(eval_item.raw_request, eval_item.raw_response)
    return traces.inject_experiment_run_id_to_trace(trace, experiment_id, run_id)


def _populate_eval_item_with_trace(eval_item: entities.EvalItem) -> entities.EvalItem:
    """
    Populate the eval item in place by extracting additional information from the trace.

    Keep the existing values in the eval item if they already exist.
    """
    # Extract tool calls from the trace, or response if trace is not available.
    eval_item.tool_calls = traces.extract_tool_calls(
        response=eval_item.raw_response, trace=eval_item.trace
    )

    # Skip if the trace is None
    if eval_item.trace is None:
        return eval_item

    eval_item.raw_response = input_output_utils.to_dict(
        traces.extract_model_output_from_trace(eval_item.trace)
    )

    eval_item.answer = (
        input_output_utils.response_to_string(
            traces.extract_model_output_from_trace(eval_item.trace)
        )
        if eval_item.answer is None
        else eval_item.answer
    )

    eval_item.retrieval_context = (
        traces.extract_retrieval_context_from_trace(eval_item.trace)
        if eval_item.retrieval_context is None
        else eval_item.retrieval_context
    )

    return eval_item


def _emit_custom_assessments_usage_event_if_present(
    client: managed_rag_client.ManagedRagClient,
    assessment_configs: List[assessment_config.AssessmentConfig],
):
    # TODO: change this to use the new usage tracking API
    evaluation_metric_configs = [
        assessment_conf
        for assessment_conf in assessment_configs
        if isinstance(
            assessment_conf, assessment_config.EvaluationMetricAssessmentConfig
        )
    ]

    if evaluation_metric_configs:
        try:
            batch_size = session.current_session().session_batch_size
            client.emit_chat_assessment_usage_event(
                evaluation_metric_configs, batch_size
            )
        except Exception:
            # Telemetry logging failures are non-fatal.
            # Don't want to indicate to users that we're emitting data
            # TODO [ML-43811]: handle this case better since it means we have a loss of billing data
            pass


def _emit_custom_metric_usage_event_if_present(
    client: managed_rag_client.ManagedRagClient,
    custom_metrics: List[agent_custom_metrics.CustomMetric],
    metric_stats: Optional[Dict[str, per_run_metrics.MetricAggregateData]] = None,
):
    if custom_metrics:
        try:
            batch_size = session.current_session().session_batch_size
            client.emit_custom_metric_usage_event(
                custom_metrics=custom_metrics,
                eval_count=batch_size,
                metric_stats=metric_stats,
            )
        except Exception:
            # Telemetry logging failures are non-fatal.
            # Don't want to indicate to users that we're emitting data
            # TODO [ML-43811]: handle this case better since it means we have a loss of billing data
            pass


def _build_rate_limiter_for_assessment() -> rate_limit.RateLimiter:
    """Build a rate limiter for the assessment."""
    # Return a no-op rate limiter if the rate limiter for assessment is not enabled
    if not env_vars.RAG_EVAL_ENABLE_RATE_LIMIT_FOR_ASSESSMENT.get():
        return rate_limit.RateLimiter.no_op()

    # For now, rate limiter config is from environment variables
    rate_limit_config = rate_limit.RateLimitConfig(
        quota=env_vars.RAG_EVAL_RATE_LIMIT_QUOTA.get(),
        time_window_in_seconds=env_vars.RAG_EVAL_RATE_LIMIT_TIME_WINDOW_IN_SECONDS.get(),
    )
    return rate_limit.RateLimiter.build(
        quota=rate_limit_config.quota,
        time_window_in_seconds=rate_limit_config.time_window_in_seconds,
    )


def log_traces_and_assessments(
    experiment_id: Optional[str],
    run_id: Optional[str],
    trace: mlflow_entities.Trace,
    assessments: List[mlflow_entities.Assessment],
) -> mlflow_entities.Trace:
    """
    Log the trace and assessments to MLflow. We do this to ensure that MLFlow has a trace for every
    eval row, storing the computed assessments/metrics.

    A trace may have been generated and logged during model invocation, in which case we don't
    need to create a trace. However, if a trace was passed in as part of the eval row, we need to
    make a copy, because we don't know if the trace was used in a previous eval invocation. Without
    a copy, we could end up with multiple evaluation runs adding assessments to the same trace.
    """
    if not env_vars.AGENT_EVAL_LOG_TRACES_TO_MLFLOW_ENABLED.get():
        return trace

    # Ensure there's always a valid experiment ID. Note this internal method will fall back to the
    # default experiment ID if there is no current experiment. In Databricks, it's the
    # notebook-based experiment and in OSS it is `experiment_id=0`.
    experiment_id = (
        fluent._get_experiment_id() if experiment_id is None else experiment_id
    )
    # Try to get the active run from the context
    run_id = context.get_context().get_mlflow_run_id() if run_id is None else run_id

    with mlflow.utils.logging_utils.suppress_logs(
        mlflow.tracing.fluent.__name__, _FAIL_TO_GET_TRACE_WARNING_MSG
    ):
        # Ensure that every trace is logged in MLflow, regardless of where it came from.
        # Specifically, if the trace is present in MLflow, do nothing. Otherwise, log the trace.
        if (
            trace.info.request_id is None
            or mlflow.get_trace(trace.info.request_id) is None
        ):
            trace.info.experiment_id = experiment_id
            if run_id is not None:
                trace.info.request_metadata[
                    tracing_constant.TraceMetadataKey.SOURCE_RUN
                ] = run_id

            mlflow_client = mlflow.tracking.MlflowClient()
            try:
                # TODO(ML-51635): Add retries to failures
                stored_trace_id = mlflow_client._log_trace(trace)
                trace.info.request_id = stored_trace_id
            except Exception as e:
                _logger.warning(f"Failed to log the trace: {e}")
                return trace

        if env_vars.AGENT_EVAL_LOG_ASSESSMENTS_TO_MLFLOW_ENABLED.get():
            # Create the assessments
            for assessment in assessments:
                # Ensure that if we created a new trace, that the updated trace_id is reflected in
                # the assessments.
                assessment.trace_id = trace.info.request_id
                assessment.metadata = (
                    {**assessment.metadata, "run_id": run_id}
                    if assessment.metadata is not None
                    else {"run_id": run_id}
                )
                _log_assessment_to_mlflow(assessment)

        # At this point, eval_result.assessments is a stale field since assessment_id is populated
        # in the backend. Get the trace to fetch newly created assessments, with assessment_ids.
        return mlflow.get_trace(trace.info.request_id)


def _log_assessment_to_mlflow(
    assessment: mlflow_entities.Assessment,
) -> Optional[mlflow_entities.Assessment]:
    """
    Creates the given assessment in MLflow.
    """
    # Note that the `log_expectation` and `log_feedback` APIs expect the ID without the "0x" prefix.
    # However, the `encode_trace_id` utility adds the "0x" prefix so we add this check.
    span_id = assessment.span_id.removeprefix("0x")
    # TODO(ML-51635): Add retries to failures
    try:
        if assessment.expectation is not None:
            return mlflow.log_expectation(
                trace_id=assessment.trace_id,
                name=assessment.name,
                source=assessment.source,
                value=assessment.expectation.value,
                metadata=assessment.metadata,
                span_id=span_id,
            )
        else:
            if assessment.error is not None:
                error = assessment.error
                value = None
            else:
                error = None
                value = assessment.feedback.value

            return mlflow.log_feedback(
                trace_id=assessment.trace_id,
                name=assessment.name,
                source=assessment.source,
                error=error,
                value=value,
                rationale=assessment.rationale,
                metadata=assessment.metadata,
                span_id=span_id,
            )
    except Exception as e:
        _logger.warning(f"Failed to log the assessment: {e}")
        return
