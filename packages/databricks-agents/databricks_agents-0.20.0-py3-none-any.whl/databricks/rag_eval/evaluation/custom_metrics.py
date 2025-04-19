import dataclasses
import functools
import inspect
import logging
import traceback
from typing import Any, Callable, Collection, Dict, List, Optional

import mlflow.metrics
from mlflow import entities as mlflow_entities
from mlflow import evaluation as mlflow_eval
from mlflow.utils.annotations import experimental

from databricks.rag_eval import schemas
from databricks.rag_eval.evaluation import entities, metrics
from databricks.rag_eval.utils import error_utils, input_output_utils

_logger = logging.getLogger(__name__)
_TOOL_CALLS = "tool_calls"


def _make_code_type_assessment_source(metric_name):
    return mlflow_eval.AssessmentSource(
        source_type=mlflow_eval.AssessmentSourceType.CODE,
        source_id=metric_name,
    )


def _validate_custom_assessment_name(*, metric_name: str, assessment_name: str):
    """Validate the name of the returned Assessments from the custom metric."""
    if not isinstance(assessment_name, str):
        raise error_utils.ValidationError(
            f"Got unsupported result from custom metric '{metric_name}'. "
            f"The name of the returned Assessment from custom metrics must be a string. "
            f"Got {assessment_name} in custom metric '{metric_name}'.",
        )
    if not assessment_name:
        raise error_utils.ValidationError(
            f"Got unsupported result from custom metric '{metric_name}'. "
            "The name of the returned Assessment from custom metrics must not be empty. "
            f"Got an empty Assessment name in custom metric '{metric_name}'.",
        )


def _normalize_custom_assessment(
    assessment: mlflow_eval.Assessment,
    metric_name: str,
) -> mlflow_eval.Assessment:
    """
    Normalize the custom assessment
    - If the source is not set, set it to the default source.
    - Prepend the metric name to the assessment name.
    """
    assessment_name = metric_name + "/" + assessment.name
    if (
        assessment.source is None
        or assessment.source.source_type
        == mlflow_entities.AssessmentSourceType.SOURCE_TYPE_UNSPECIFIED
    ):
        assessment_source = _make_code_type_assessment_source(metric_name)
    else:
        assessment_source = assessment.source

    assessment = mlflow_eval.Assessment(
        name=assessment_name,
        source=assessment_source,
        value=assessment.value,
        rationale=assessment.rationale,
        metadata=assessment.metadata,
        error_code=assessment.error_code,
        error_message=assessment.error_message,
    )

    _validate_custom_assessment_name(
        metric_name=metric_name, assessment_name=assessment.name
    )
    return assessment


def _get_full_args_for_custom_metric(eval_item: entities.EvalItem) -> Dict[str, Any]:
    """Get the all available arguments for the custom metrics."""
    return {
        schemas.REQUEST_ID_COL: eval_item.question_id,
        # Here we wrap the raw request in a ChatCompletionRequest object if it's a plain string to be consistent
        # because we have the same wrapping logic when invoking the model.
        # In the long term future, we want to remove this wrapping logic and pass the raw request as is.
        schemas.REQUEST_COL: input_output_utils.to_chat_completion_request(
            eval_item.raw_request
        ),
        schemas.RESPONSE_COL: eval_item.raw_response,
        schemas.RETRIEVED_CONTEXT_COL: (
            eval_item.retrieval_context.to_output_dict()
            if eval_item.retrieval_context
            else None
        ),
        schemas.EXPECTED_RESPONSE_COL: eval_item.ground_truth_answer,
        schemas.EXPECTED_FACTS_COL: eval_item.expected_facts,
        schemas.GUIDELINES_COL: eval_item.guidelines,
        schemas.EXPECTED_RETRIEVED_CONTEXT_COL: (
            eval_item.ground_truth_retrieval_context.to_output_dict()
            if eval_item.ground_truth_retrieval_context
            else None
        ),
        schemas.CUSTOM_EXPECTED_COL: eval_item.custom_expected,
        schemas.CUSTOM_INPUTS_COL: eval_item.custom_inputs,
        schemas.CUSTOM_OUTPUTS_COL: eval_item.custom_outputs,
        schemas.TRACE_COL: eval_item.trace,
        schemas.TOOL_CALLS_COL: eval_item.tool_calls,
    }


def _convert_custom_metric_value(
    metric_name: str, metric_value: Any
) -> List[mlflow_eval.Assessment]:
    """
    Convert the custom metric value to a list of MLflow Assessments.
    Raise an error if the value is not valid.

    Supported metric values:
        - number
        - boolean
        - string
        - Assessment object
        - List[Assessment]


    If you have a number, boolean, or string:
    @metric
    def custom_metric(request_id, request, response):
        return 0.5

    The assessment will be normalized to:
        mlflow_eval.Assessment(
            name="metric/custom_metric",
            value=0.5,
            source=mlflow_eval.AssessmentSource(
                source_type=mlflow_eval.AssessmentSourceType.CODE,
                source_id="metric/custom_metric",
            ),
        )

    If you have an assessment or list of assessments:
    @metric
    def custom_metric(request_id, request, response):
        return mlflow_eval.Assessment(
            name="custom_assessment",
            value=0.5,
        )
    The assessment will be normalized to:
        mlflow_eval.Assessment(
            name="metric/custom_metric/custom_assessment",
            value=0.5,
            source=mlflow_eval.AssessmentSource(
                source_type=mlflow_eval.AssessmentSourceType.CODE,
                source_id="metric/custom_metric",
            ),
        )
    """
    # None is a valid metric value, return an empty list
    if metric_value is None:
        return []

    # Primitives are valid metric values
    if isinstance(metric_value, (int, float, bool, str)):
        return [
            mlflow_eval.Assessment(
                name=metric_name,
                value=metric_value,
                source=_make_code_type_assessment_source(metric_name),
            )
        ]

    if isinstance(metric_value, mlflow_eval.Assessment):
        return [_normalize_custom_assessment(metric_value, metric_name)]

    if isinstance(metric_value, Collection):
        assessments = []
        seen_assessment_names = set()  # Ensure the assessment names are unique
        for item in metric_value:
            if not isinstance(item, mlflow_eval.Assessment):
                raise error_utils.ValidationError(
                    f"Got unsupported result from custom metric '{metric_name}'. "
                    f"Expected the metric value to be a number, or a boolean, or a string, or an Assessment, or a list of Assessments. "
                    f"Got {type(item)} in the list. Full list: {metric_value}.",
                )
            normalized_assessment = _normalize_custom_assessment(item, metric_name)
            if normalized_assessment.name in seen_assessment_names:
                raise error_utils.ValidationError(
                    f"Got unsupported result from custom metric '{metric_name}'. "
                    f"The names of the returned list of Assessments from custom metrics must be unique. "
                    f"Got duplicate Assessment name '{normalized_assessment.name}'.",
                )
            seen_assessment_names.add(normalized_assessment.name)
            assessments.append(normalized_assessment)
        return assessments

    raise error_utils.ValidationError(
        f"Got unsupported result from custom metric '{metric_name}'. "
        f"Expected the metric value to be a number, or a boolean, or a string, or an Assessment, or a list of Assessments. "
        f"Got {metric_value}.",
    )


@dataclasses.dataclass
class CustomMetric(metrics.Metric):
    """
    A custom metric that runs a user-defined evaluation function.

    :param name: The name of the metric.
    :param eval_fn: A user-defined function that computes the metric value.
    """

    name: str
    eval_fn: Callable[..., Any]

    def run(
        self,
        *,
        eval_item: Optional[entities.EvalItem] = None,
        assessment_results: Optional[List[entities.AssessmentResult]] = None,
    ) -> List[entities.MetricResult]:
        if eval_item is None:
            return []

        # Add prefix to ensure the name does not conflict with built-in metrics
        metric_name = schemas.CUSTOM_METRICS_PREFIX + self.name

        kwargs = self._get_kwargs(eval_item)
        try:
            # noinspection PyCallingNonCallable
            metric_value = self.eval_fn(**kwargs)
        except Exception as e:
            _logger.error(
                "Error when evaluating metric %s: %s.\n%s",
                self.name,
                e,
                traceback.format_exc(),
            )
            error_assessment = mlflow_eval.Assessment(
                name=metric_name,
                source=_make_code_type_assessment_source(metric_name),
                error_code="CUSTOM_METRIC_ERROR",
                error_message=str(e),
            )
            return [
                entities.MetricResult(
                    metric_value=error_assessment,
                )
            ]

        assessments = _convert_custom_metric_value(metric_name, metric_value)
        return [
            entities.MetricResult(
                metric_value=assessment,
            )
            for assessment in assessments
        ]

    def __call__(self, *args, **kwargs):
        return self.eval_fn(*args, **kwargs)

    def _get_kwargs(self, eval_item: entities.EvalItem) -> Dict[str, Any]:
        # noinspection PyTypeChecker
        arg_spec = inspect.getfullargspec(self.eval_fn)

        full_args = _get_full_args_for_custom_metric(eval_item)
        # If the metric accepts **kwargs, pass all available arguments
        if arg_spec.varkw:
            return full_args
        kwonlydefaults = arg_spec.kwonlydefaults or {}
        required_args = arg_spec.args + [
            arg for arg in arg_spec.kwonlyargs if arg not in kwonlydefaults
        ]
        optional_args = list(kwonlydefaults.keys())
        accepted_args = required_args + optional_args
        # Validate that the dataframe can cover all the required arguments
        missing_args = set(required_args) - full_args.keys()
        if missing_args:
            raise TypeError(
                f"Dataframe is missing arguments {missing_args} to metric {self.name}"
            )
        # Filter the dataframe down to arguments that the metric accepts
        return {k: v for k, v in full_args.items() if k in accepted_args}


@experimental
def metric(eval_fn=None, *, name: Optional[str] = None):
    # noinspection PySingleQuotedDocstring
    '''
    Create a custom agent metric from a user-defined eval function.

    Can be used as a decorator on the eval_fn.

    The eval_fn should have the following signature:

        .. code-block:: python

            def eval_fn(
                *,
                request_id: str,
                request: Union[ChatCompletionRequest, str],
                response: Optional[Any],
                retrieved_context: Optional[List[Dict[str, str]]]
                expected_response: Optional[Any],
                expected_facts: Optional[List[str]],
                expected_retrieved_context: Optional[List[Dict[str, str]]],
                custom_expected: Optional[Dict[str, Any]],
                custom_inputs: Optional[Dict[str, Any]],
                custom_outputs: Optional[Dict[str, Any]],
                trace: Optional[mlflow.entities.Trace],
                tool_calls: Optional[List[ToolCallInvocation]],
                **kwargs,
            ) -> Optional[Union[int, float, bool]]:
                """
                Args:
                    request_id: The ID of the request.
                    request: The agent's input from your input eval dataset.
                    response: The agent's raw output. Whatever we get from the agent, we will pass it here as is.
                    retrieved_context: Retrieved context, can be from your input eval dataset or from the trace,
                                       we will try to extract retrieval context from the trace;
                                       if you have custom extraction logic, use the `trace` field.
                    expected_response: The expected response from your input eval dataset.
                    expected_facts: The expected facts from your input eval dataset.
                    expected_retrieved_context: The expected retrieved context from your input eval dataset.
                    custom_expected: Custom expected information from your input eval dataset.
                    custom_inputs: Custom inputs from your input eval dataset.
                    custom_outputs: Custom outputs from the agent's response.
                    trace: The trace object. You can use this to extract additional information from the trace.
                    tool_calls: List of tool call invocations, can be from your agent's response (ChatAgent only)
                                or from the trace. We will prioritize extracting from the trace as it contains
                                additional information such as available tools and from which span the tool was called.
                """

    eval_fn will always be called with named arguments. You only need to declare the arguments you need.
    If kwargs is declared, all available arguments will be passed.

    The return value of the function should be either a number or a boolean. It will be used as the metric value.
    Return None if the metric cannot be computed.

    :param eval_fn: The user-defined eval function.
    :param name: The name of the metric. If not provided, the function name will be used.
    '''

    def decorator(fn, *, _name=name):
        # Use mlflow.metrics.make_metric to validate the metric name
        mlflow.metrics.make_metric(eval_fn=fn, greater_is_better=True, name=_name)
        metric_name = _name or fn.__name__

        # Validate signature of the fn
        arg_spec = inspect.getfullargspec(fn)
        if arg_spec.varargs:
            raise error_utils.ValidationError(
                "The eval_fn should not accept *args.",
            )
        return functools.wraps(fn)(CustomMetric(name=metric_name, eval_fn=fn))

    if eval_fn is not None:
        return decorator(eval_fn)

    return decorator
