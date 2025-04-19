from typing import Any, Collection, Optional

from mlflow import evaluation as mlflow_eval

from databricks.rag_eval.config import assessment_config
from databricks.rag_eval.evaluation import entities

_MESSAGE_OVERRIDE = "message_override"

CHUNK_PRECISION_IS_LOW_MESSAGE = (
    "The root cause of failure is traced to the negative ratings of "
    f"{assessment_config.CHUNK_RELEVANCE.assessment_name} which marked all retrieved "
    "chunks as irrelevant to the question. "
    f"See the {assessment_config.CHUNK_RELEVANCE.assessment_name} rationale for more details."
)

PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative per-chunk ratings of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

DEFAULT_FAIL_MESSAGE = (
    "The root cause of failure is traced to the negative rating of {judge_name}. "
    "See the {judge_name} rationale for more details."
)

SUGGESTED_ACTIONS = {
    assessment_config.CONTEXT_SUFFICIENCY.assessment_name: (
        "First, you should ensure that the vector DB contains the "
        "missing information. Second, you should tune your retrieval "
        "step to retrieve the missing information (see the judges' rationales to understand what's missing). "
        "Here are some methods that you can try for this: retrieving more chunks, trying different embedding models, "
        "or over-fetching & reranking results."
    ),
    assessment_config.CHUNK_RELEVANCE.assessment_name: (
        "First, you should ensure that relevant chunks are present in the "
        "vector DB. Second, you should tune your retrieval step to retrieve the missing information (see the judges' "
        "rationales to understand what's missing). Here are some methods that you can try for this: "
        "retrieving more chunks, trying different embedding models, or over-fetching & reranking results."
    ),
    assessment_config.HARMFULNESS.assessment_name: (
        "Consider implementing guardrails to prevent harmful content or a "
        "post-processing step to filter out harmful content."
    ),
    assessment_config.RELEVANCE_TO_QUERY.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier "
        "in the prompt, or using a more capable LLM."
    ),
    assessment_config.GROUNDEDNESS.assessment_name: (
        "Consider updating the prompt template to emphasize "
        "reliance on retrieved context, using a more capable LLM, or implementing a post-generation "
        "verification step."
    ),
    assessment_config.CORRECTNESS.assessment_name: (
        "Consider improving the prompt template to encourage direct, "
        "specific responses, re-ranking retrievals to provide more relevant chunks to the LLM earlier in "
        "the prompt, or using a more capable LLM."
    ),
    assessment_config.GUIDELINE_ADHERENCE.assessment_name: (
        "See the guideline_adherence rationale for more details on the failure."
    ),
}


def compute_overall_assessment(
    assessment_results: Collection[entities.AssessmentResult],
    metric_results: Collection[entities.MetricResult],
) -> Optional[entities.OverallAssessment]:
    """
    Compute the overall assessment based on the individual assessment results and applying our RCA logic.
    """
    assessments = []
    for result in assessment_results + metric_results:
        assessment = result.to_mlflow_assessment_v2()
        if isinstance(assessment, mlflow_eval.Assessment):
            assessments.append(assessment)
        elif isinstance(assessment, list) and len(assessment):
            assessments.append(_consolidate_per_chunk_assessment(assessment))

    return _compute_overall_assessment(assessments)


# ================ Overall assessment ================
def construct_fail_assessment(
    assessment: mlflow_eval.Assessment,
) -> entities.OverallAssessment:
    """
    Construct fail assessment with an RCA from the given assessment.

    The rationale of the failed assessment has the following format for builtin-judges:
    "[judge_name] {message}. *Suggested Action*: {action}".

    For custom judges, the rationale is: "[judge_name] {message}".

    The "message" part is defined as follows:
    - DEFAULT_FAIL_MESSAGE for per-request assessments, with the judge name substituted.
    - CHUNK_PRECISION_IS_LOW_MESSAGE for chunk relevance.
    - PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE for other per-chunk assessments.

    The action for built-in judges is defined in SUGGESTED_ACTIONS.
    """
    judge_name = assessment.name
    message = DEFAULT_FAIL_MESSAGE.format(judge_name=judge_name)
    if assessment.metadata is not None:
        message_override = assessment.metadata.get(_MESSAGE_OVERRIDE)
        message = message_override if message_override is not None else message

    rationale = f"[{judge_name}] {message}"

    action = SUGGESTED_ACTIONS.get(judge_name)
    if action is not None:
        rationale += f" **Suggested Actions**: {action}"

    return entities.OverallAssessment(
        rating=entities.Rating.value(
            categorical_value=entities.CategoricalRating.NO,
            rationale=rationale,
        ),
        root_cause_assessment=judge_name,
        root_cause_rationale=message,
        suggested_action=action,
    )


def construct_pass_assessment() -> entities.OverallAssessment:
    """Construct pass assessment."""
    return entities.OverallAssessment(
        rating=entities.Rating.value(
            categorical_value=entities.CategoricalRating.YES,
        ),
    )


def _compute_overall_assessment(
    assessments: Collection[mlflow_eval.Assessment],
) -> Optional[entities.OverallAssessment]:
    """
    Compute the overall assessment based on the individual assessment results and applying our RCA logic.

    The categorical rating contains a high-level tag describing quality issues. If our logic does
    not recognize the set of judges, we return `YES` or `NO` based on a logical AND of all judges.
    Note that all errors are ignored in the logical AND.

    The rationale contains the root cause analysis (RCA) and potential fixes based on the assessment
    results. If all judges are passing, the RCA will be empty.
    """
    # Filter out errored per-request assessments or fully errored per-chunk assessments out of RCA
    # Also filters out assessments without categorical values (e.g., assessments returning floats, bools, etc)
    # Note: we do not assume whether boolean outputs are good/bad, so we only consider explicit categorical ratings.
    filtered_assessments = [
        assessment
        for assessment in assessments
        if (
            assessment.error_code is None
            and (
                entities.CategoricalRating(str(assessment.value))
                != entities.CategoricalRating.UNKNOWN
            )
        )
    ]
    if not len(filtered_assessments):
        return None

    assessments_mapping = {
        assessment.name: assessment for assessment in filtered_assessments
    }

    # Find the first negative assessment
    first_negative_assessment = next(
        (
            assessment
            for assessment in filtered_assessments
            if _assessment_is_fail(assessment)
        ),
        None,
    )

    # Early return if there are no negative assessments.
    if first_negative_assessment is None:
        return construct_pass_assessment()

    # RCA logic. We will check judges in the following order to find the first one that fails.
    assessments_to_check = [
        assessment_config.CONTEXT_SUFFICIENCY.assessment_name,
        assessment_config.CHUNK_RELEVANCE.assessment_name,
        assessment_config.GROUNDEDNESS.assessment_name,
        assessment_config.CORRECTNESS.assessment_name,
        assessment_config.RELEVANCE_TO_QUERY.assessment_name,
        assessment_config.HARMFULNESS.assessment_name,
        assessment_config.GUIDELINE_ADHERENCE.assessment_name,
    ]
    for assessment_name in assessments_to_check:
        assessment = assessments_mapping.get(assessment_name)
        if _assessment_is_fail(assessment):
            return construct_fail_assessment(assessment)

    # Built-in logic passes, so some custom judge failed. Return a rating indicating the first failed judge.
    return construct_fail_assessment(first_negative_assessment)


def _value_is_fail(value: Any) -> bool:
    """Check if a value corresponds to a failure."""
    if value is None:
        return False
    return value == entities.CategoricalRating.NO


def _assessment_is_fail(assessment: Optional[mlflow_eval.Assessment]) -> bool:
    """Check if an assessment result corresponds to a failure."""
    if assessment is None:
        return False
    return _value_is_fail(assessment.value)


def _consolidate_per_chunk_assessment(
    assessments: Collection[mlflow_eval.Assessment],
) -> mlflow_eval.Assessment:
    """
    Consolidates per-chunk assessments into a single assessment value. For a per-chunk assessment to fail, at least one
    rating should be NO, except for chunk relevance, for which all ratings must be NO.
    :param assessment_map: Positional map of per-chunk assessments
    :return: Single consolidated assessment
    """
    judge_name = assessments[0].name
    positional_ratings_are_fail = [
        _value_is_fail(assessment.value) for assessment in assessments
    ]

    if judge_name == assessment_config.CHUNK_RELEVANCE.assessment_name:
        is_fail = all(positional_ratings_are_fail)
        message_override = CHUNK_PRECISION_IS_LOW_MESSAGE
    else:
        is_fail = any(positional_ratings_are_fail)
        message_override = PER_CHUNK_ASSESSMENTS_FAIL_MESSAGE.format(
            judge_name=judge_name
        )

    # TODO(ML-51637): Deprecate usage of MLflow v2 assessments
    return mlflow_eval.Assessment(
        name=judge_name,
        value=(
            entities.CategoricalRating.NO if is_fail else entities.CategoricalRating.YES
        ),
        # Use the metadata to override the default message with a retrieval-specific one.
        metadata={_MESSAGE_OVERRIDE: message_override},
    )
