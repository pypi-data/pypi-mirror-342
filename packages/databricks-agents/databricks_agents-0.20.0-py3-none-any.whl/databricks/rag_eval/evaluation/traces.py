"""This module deals with trace and extracting information from traces."""

import dataclasses
import json
import logging
import time
import uuid
from typing import Any, Dict, List, Mapping, Optional

import mlflow.entities as mlflow_entities
import mlflow.models.dependencies_schemas as mlflow_dependencies_schemas
import mlflow.tracing.constant as mlflow_tracing_constant
from mlflow.tracing.utils import (
    build_otel_context,
    decode_id,
)
from opentelemetry.sdk.trace import ReadableSpan as OTelReadableSpan
from opentelemetry.sdk.trace import Status, StatusCode

from databricks.rag_eval.evaluation import entities
from databricks.rag_eval.utils import input_output_utils

_logger = logging.getLogger(__name__)


_TRACE_REQUEST_METADATA_LEN_LIMIT = 250
_DEFAULT_DOC_URI_COL = "doc_uri"

_ID = "id"  # Generic ID field, used for tool call ID
_MESSAGES = "messages"

_ROLE = "role"
_ASSISTANT_ROLE = "assistant"
_TOOL_ROLE = "tool"

_TOOL_FUNCTION = "function"
_TOOL_FUNCTION_NAME = "name"
_TOOL_FUNCTION_ARGUMENTS = "arguments"
_TOOL_CALLS = "tool_calls"
_TOOL_CALL_ID = "tool_call_id"


def _span_is_type(
    span: mlflow_entities.Span,
    span_type: str | List[str],
) -> bool:
    """Check if the span is of a certain span type or one of the span types in the collection"""
    if span.attributes is None:
        return False
    if not isinstance(span_type, List):
        span_type = [span_type]
    return (
        span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.SPAN_TYPE)
        in span_type
    )


# ================== Retrieval Context ==================
def extract_retrieval_context_from_trace(
    trace: Optional[mlflow_entities.Trace],
) -> Optional[entities.RetrievalContext]:
    """
    Extract the retrieval context from the trace.

    Only consider the last retrieval span in the trace if there are multiple retrieval spans.

    If the trace does not have a retrieval span, return None.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return None.

    :param trace: The trace
    :return: The retrieval context
    """
    if trace is None or trace.data is None:
        return None

    # Only consider the top-level retrieval spans
    top_level_retrieval_spans = _get_top_level_retrieval_spans(trace)
    if len(top_level_retrieval_spans) == 0:
        return None
    # Only consider the last top-level retrieval span
    retrieval_span = top_level_retrieval_spans[-1]

    # Get the retriever schema from the trace info
    retriever_schema = _get_retriever_schema_from_trace(trace.info)
    return _extract_retrieval_context_from_retrieval_span(
        retrieval_span, retriever_schema
    )


def _get_top_level_retrieval_spans(
    trace: mlflow_entities.Trace,
) -> List[mlflow_entities.Span]:
    """
    Get the top-level retrieval spans in the trace.
    Top-level retrieval spans are the retrieval spans that are not children of other retrieval spans.

    For example, given the following spans:
    - Span A (Chain)
      - Span B (Retriever)
        - Span C (Retriever)
      - Span D (Retriever)
        - Span E (LLM)
          - Span F (Retriever)
    Span B and Span D are top-level retrieval spans.
    Span C and Span F are NOT top-level retrieval spans because they are children of other retrieval spans.
    """
    if trace.data is None or not trace.data.spans:
        return []

    retrieval_spans = {
        span.span_id: span
        for span in trace.search_spans(mlflow_entities.SpanType.RETRIEVER)
    }

    top_level_retrieval_spans = []

    for span in retrieval_spans.values():
        # Check if this span is a child of another retrieval span
        parent_id = span.parent_id
        while parent_id:
            if parent_id in retrieval_spans.keys():
                # This span is a child of another retrieval span
                break
            parent_span = next(
                (s for s in trace.data.spans if s.span_id == parent_id), None
            )
            if parent_span is None:
                # The parent span is not found, malformed trace
                break
            parent_id = parent_span.parent_id
        else:
            # If the loop completes without breaking, this is a top-level span
            top_level_retrieval_spans.append(span)

    return top_level_retrieval_spans


def _get_retriever_schema_from_trace(
    trace_info: Optional[mlflow_entities.TraceInfo],
) -> Optional[mlflow_dependencies_schemas.RetrieverSchema]:
    """
    Get the retriever schema from the trace info tags.

    Retriever schema is stored in the trace info tags as a JSON string of list of retriever schemas.
    Only consider the last retriever schema if there are multiple retriever schemas.
    """
    if (
        trace_info is None
        or trace_info.tags is None
        or mlflow_dependencies_schemas.DependenciesSchemasType.RETRIEVERS.value
        not in trace_info.tags
    ):
        return None
    retriever_schemas = json.loads(
        trace_info.tags[
            mlflow_dependencies_schemas.DependenciesSchemasType.RETRIEVERS.value
        ]
    )
    # Only consider the last retriever schema
    return (
        mlflow_dependencies_schemas.RetrieverSchema.from_dict(retriever_schemas[-1])
        if isinstance(retriever_schemas, list) and len(retriever_schemas) > 0
        else None
    )


def _extract_retrieval_context_from_retrieval_span(
    span: mlflow_entities.Span,
    retriever_schema: Optional[mlflow_dependencies_schemas.RetrieverSchema],
) -> Optional[entities.RetrievalContext]:
    """Get the retrieval context from a retrieval span."""
    try:
        doc_uri_col = (
            retriever_schema.doc_uri
            if retriever_schema and retriever_schema.doc_uri
            else _DEFAULT_DOC_URI_COL
        )
        retriever_outputs = span.attributes.get(
            mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
        )
        return entities.RetrievalContext(
            [
                (
                    entities.Chunk(
                        doc_uri=(
                            chunk.get("metadata", {}).get(doc_uri_col)
                            if chunk
                            else None
                        ),
                        content=chunk.get("page_content") if chunk else None,
                    )
                )
                for chunk in retriever_outputs or []
            ]
        )
    except Exception as e:
        _logger.debug(f"Fail to get retrieval context from span: {span}. Error: {e!r}")
        return None


# ================== Token Count ==================
@dataclasses.dataclass
class SpanTokenCount:
    prompt_token_count: Optional[int] = None
    completion_token_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpanTokenCount":
        return cls(
            prompt_token_count=data.get("prompt_tokens", None),
            completion_token_count=data.get("completion_tokens", None),
        )


@dataclasses.dataclass
class TraceTokenCount:
    input_token_count: Optional[int] = None
    output_token_count: Optional[int] = None

    @property
    def total_token_count(self) -> int:
        if self.input_token_count is not None and self.output_token_count is not None:
            return self.input_token_count + self.output_token_count
        return None


def compute_total_token_count(
    trace: Optional[mlflow_entities.Trace],
) -> TraceTokenCount:
    """
    Compute the total input/output tokens across all trace spans.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return empty TraceTokenCount.

    :param trace: The trace object

    :return: Total input/output token counts
    """
    if trace is None or trace.data is None:
        return TraceTokenCount()

    # Only consider leaf spans that is of type LLM or CHAT_MODEL.
    # Depending on the implementation of LLM/CHAT_MODEL components,
    # a span may have multiple children spans that are also LLM/CHAT_MODEL spans.
    # But only the leaf spans send requests to the LLM.
    # To avoid double counting, we only consider leaf spans.
    leaf_spans = _get_leaf_spans(trace)
    leaf_llm_or_chat_model_spans = [
        span
        for span in leaf_spans
        if _span_is_type(
            span, [mlflow_entities.SpanType.LLM, mlflow_entities.SpanType.CHAT_MODEL]
        )
    ]

    input_token_counts = []
    output_token_counts = []
    for span in leaf_llm_or_chat_model_spans:
        span_token_count = _extract_span_token_counts(span)
        # Input
        if span_token_count.prompt_token_count is not None:
            input_token_counts.append(span_token_count.prompt_token_count)
        # Output
        if span_token_count.completion_token_count is not None:
            output_token_counts.append(span_token_count.completion_token_count)
    return TraceTokenCount(
        input_token_count=(
            sum(input_token_counts) if len(input_token_counts) > 0 else None
        ),
        output_token_count=(
            sum(output_token_counts) if len(output_token_counts) > 0 else None
        ),
    )


def _extract_span_token_counts(span: mlflow_entities.Span) -> SpanTokenCount:
    """Extract the token counts from the LLM/CHAT_MODEL span."""
    if (
        span.attributes is None
        or mlflow_tracing_constant.SpanAttributeKey.OUTPUTS not in span.attributes
    ):
        return SpanTokenCount()
    try:
        # See https://python.langchain.com/docs/modules/callbacks/#callback-handlers for output format
        # of CHAT_MODEL and LLM spans in LangChain
        if _span_is_type(
            span, [mlflow_entities.SpanType.CHAT_MODEL, mlflow_entities.SpanType.LLM]
        ):
            # The format of the output attribute for LLM/CHAT_MODEL is a ChatResult. Typically, the
            # token usage is either stored in 'usage' or 'llm_output' (ChatDatabricks in LangChain).
            # e.g. { 'llm_output': {'total_tokens': ...}, ... }
            span_outputs = span.attributes[
                mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
            ]
            if "llm_output" in span_outputs:
                return SpanTokenCount.from_dict(span_outputs["llm_output"])
            elif "usage" in span_outputs:
                return SpanTokenCount.from_dict(span_outputs["usage"])
            else:
                return SpanTokenCount()
        else:
            # Span is not a LLM/CHAT_MODEL span, nothing to extract
            return SpanTokenCount()

    except Exception as e:
        _logger.debug(f"Fail to extract token counts from span: {span}. Error: {e!r}")
        return SpanTokenCount()


# ================== Model Input/Output ==================
def extract_model_output_from_trace(
    trace: Optional[mlflow_entities.Trace],
) -> Optional[input_output_utils.ModelOutput]:
    """
    Extract the model output from the trace.

    Model output should be recorded in the root span of the trace.

    ⚠️ Warning: Please make sure to not throw exception. If fails, return None.
    """
    if trace is None:
        return None
    root_span = _get_root_span(trace)
    if root_span is None:
        return None

    try:
        if (
            root_span.attributes is None
            or mlflow_tracing_constant.SpanAttributeKey.OUTPUTS
            not in root_span.attributes
        ):
            return None
        return root_span.attributes[mlflow_tracing_constant.SpanAttributeKey.OUTPUTS]

    except Exception as e:
        _logger.debug(
            f"Fail to extract model output from the root span: {root_span}. Error: {e!r}"
        )
        return None


# ================== Tool Calls ==================
def _extract_tool_calls_from_messages(
    messages: List[Dict[str, Any]],
) -> List[entities.ToolCallInvocation]:
    """
    Helper to extract the tool calls from a list of messages. Uses the tool call ID to match tool
    calls from assistant messages to tool call results from tool messages. Note that there is no
    notion of tool spans, so we cannot extract the raw tool span.
    :param messages: List of messages
    :return: List of tool call invocations
    """
    assistant_messages_with_tools = [
        message
        for message in messages
        if message[_ROLE] == _ASSISTANT_ROLE and message.get(_TOOL_CALLS)
    ]

    tool_call_results = {
        message[_TOOL_CALL_ID]: message
        for message in messages
        if message[_ROLE] == _TOOL_ROLE
    }

    tool_call_invocations = []
    for message in assistant_messages_with_tools:
        for tool_call in message.get(_TOOL_CALLS) or []:
            tool_call_id = tool_call[_ID]
            tool_call_function = tool_call[_TOOL_FUNCTION]
            tool_call_args = tool_call_function[_TOOL_FUNCTION_ARGUMENTS]
            if isinstance(tool_call_args, str):
                try:
                    tool_call_args = json.loads(tool_call_args)
                except Exception:
                    pass

            tool_call_invocations.append(
                entities.ToolCallInvocation(
                    tool_name=tool_call_function[_TOOL_FUNCTION_NAME],
                    tool_call_args=tool_call_args,
                    tool_call_id=tool_call_id,
                    tool_call_result=tool_call_results.get(tool_call_id),
                )
            )
    return tool_call_invocations


def _extract_tool_calls_from_tool_spans(
    trace: mlflow_entities.Trace,
) -> List[entities.ToolCallInvocation]:
    """
    Helper to extract tool calls from tool spans in the trace. Note that there is no way to connect
    the tool span to the LLM/ChatModel span to get available tools.
    :param trace: The trace
    :return: List of tool call invocations
    """
    tool_spans = trace.search_spans(mlflow_entities.SpanType.TOOL)
    tool_call_invocations = []
    for span in tool_spans:
        span_inputs = span.attributes[mlflow_tracing_constant.SpanAttributeKey.INPUTS]
        span_outputs = span.attributes[mlflow_tracing_constant.SpanAttributeKey.OUTPUTS]

        tool_call_invocations.append(
            entities.ToolCallInvocation(
                tool_name=span.name,
                tool_call_args=span_inputs,
                tool_call_id=(span_outputs or {}).get(_TOOL_CALL_ID),
                tool_call_result=span_outputs,
                raw_span=span,
            )
        )

    return tool_call_invocations


def _extract_tool_calls_from_chat_model_spans(
    trace: mlflow_entities.Trace,
) -> List[entities.ToolCallInvocation]:
    """
    Helper to extract tool calls from chat model spans in the trace. Note that this method
    relies on new fields introducing in mlflow 2.20.0 to extract standardized messages and
    available tools.
    :param trace: The trace
    :return: List of tool call invocations
    """
    chat_model_spans = trace.search_spans(mlflow_entities.SpanType.CHAT_MODEL)

    tool_call_id_to_available_tools = {}
    # These dictionaries store both the invocation/result and respective spans. We store
    # the span such that we can prioritize the result span over invocation span.
    tool_call_id_to_invocation = {}
    tool_call_id_to_result = {}

    for span in chat_model_spans:
        messages = (
            span.attributes.get(mlflow_tracing_constant.SpanAttributeKey.CHAT_MESSAGES)
            or []
        )
        for idx, message in enumerate(messages):
            # The assistant has generated some tool call invocations
            if message[_ROLE] == _ASSISTANT_ROLE and _TOOL_CALLS in message:
                for tool_call in message[_TOOL_CALLS]:
                    tool_call_id = tool_call[_ID]
                    # We should use the first available span (i.e., don't overwrite this value)
                    if tool_call_id not in tool_call_id_to_invocation:
                        tool_call_id_to_invocation[tool_call_id] = (tool_call, span)

                    # If the tool call invocation is the last message, then this span
                    # contains the available tools that can be invoked. Otherwise,
                    # we cannot assume it came from the same span.
                    available_tools = span.attributes.get(
                        mlflow_tracing_constant.SpanAttributeKey.CHAT_TOOLS
                    )
                    if available_tools and idx == len(messages) - 1:
                        tool_call_id_to_available_tools[tool_call_id] = available_tools

            # The tool has responded with a tool call result
            if message[_ROLE] == _TOOL_ROLE:
                tool_call_id = message[_TOOL_CALL_ID]
                # We should use the first available span (i.e., don't overwrite this value)
                if tool_call_id not in tool_call_id_to_result:
                    tool_call_id_to_result[tool_call_id] = (message, span)

    tool_call_invocations = []
    for tool_call_id, (
        tool_call_invocation,
        invocation_span,
    ) in tool_call_id_to_invocation.items():
        tool_call_function = tool_call_invocation.get(_TOOL_FUNCTION) or {}
        tool_call_args = tool_call_function[_TOOL_FUNCTION_ARGUMENTS]
        tool_call_result, result_span = tool_call_id_to_result.get(
            tool_call_id, (None, None)
        )

        tool_call_invocations.append(
            entities.ToolCallInvocation(
                tool_name=tool_call_function[_TOOL_FUNCTION_NAME],
                tool_call_args=(
                    json.loads(tool_call_args)
                    if isinstance(tool_call_args, str)
                    else tool_call_args
                ),
                tool_call_id=tool_call_id,
                tool_call_result=tool_call_result,
                # This will prefer the span containing both result + invocation over just
                # the invocation span
                raw_span=result_span or invocation_span,
                available_tools=tool_call_id_to_available_tools.get(tool_call_id),
            )
        )

    return tool_call_invocations


def extract_tool_calls(
    *,
    response: Optional[Dict[str, Any]] = None,
    trace: Optional[mlflow_entities.Trace] = None,
) -> Optional[List[entities.ToolCallInvocation]]:
    """
    Extract tool calls from a response or trace object. The trace is prioritized as it provides more
    metadata about the tool calls and not all tools may be logged in the request.
    :param response: The response object
    :param trace: The trace object
    :return: List of tool call invocations
    """
    try:
        # We prefer extracting from the trace opposed to a response object
        if trace is not None:
            if not isinstance(trace, mlflow_entities.Trace):
                raise ValueError(
                    f"Expected a `mlflow.entities.Trace` object, got {type(trace)}"
                )
            tool_calls_from_traces = _extract_tool_calls_from_chat_model_spans(trace)
            # Try extracting from the chat model spans. If no tools are found, try using the tool spans.
            return (
                tool_calls_from_traces
                if len(tool_calls_from_traces)
                else _extract_tool_calls_from_tool_spans(trace)
            )

        if response is not None:
            if not isinstance(response, Dict):
                raise ValueError(f"Expected a dictionary, got {type(response)}")
            if _MESSAGES not in response:
                raise ValueError(
                    f"Invalid response object is missing field '{_MESSAGES}': {response}"
                )
            if not isinstance(response[_MESSAGES], list):
                raise ValueError(
                    f"Expected a list of messages, got {type(response[_MESSAGES])}"
                )

            return _extract_tool_calls_from_messages(response[_MESSAGES])

        raise ValueError("A response or trace object must be provided.")
    except Exception:
        return None


# ================== Trace Creation/Modification ==================
def create_minimal_trace(
    request: Dict[str, Any], response: Any
) -> mlflow_entities.Trace:
    """
    Create a minimal trace object with a single span, based on given request/response.
    This trace is not associated with any run or experiment.

    :param request: The request object. This is expected to be a JSON-serializable object
    :param response: The response object. This is expected to be a JSON-serializable object, but we cannot guarantee this
    :return: A new trace object.
    """
    serialized_request = (
        json.dumps(request, default=lambda o: o.__dict__)
        if not isinstance(request, str)
        else request
    )
    # Do a best-effort conversion to dump the raw model output, otherwise just dump the string
    try:
        serialized_response = (
            json.dumps(response, default=lambda o: o.__dict__)
            if not isinstance(response, str)
            else response
        )
    except:
        serialized_response = str(response)

    request_metadata = {
        mlflow_tracing_constant.TraceMetadataKey.INPUTS: serialized_request[
            :_TRACE_REQUEST_METADATA_LEN_LIMIT
        ],
        mlflow_tracing_constant.TraceMetadataKey.OUTPUTS: serialized_response[
            :_TRACE_REQUEST_METADATA_LEN_LIMIT
        ],
    }

    # We force-serialize the request/response to fit into OpenTelemetry attributes, which require
    # JSON-serialized values.
    attribute_request = json.dumps(request, default=lambda o: o.__dict__)
    # Do a best-effort conversion to dump the raw model output, otherwise just dump the string
    try:
        attribute_response = json.dumps(response, default=lambda o: o.__dict__)
    except:
        attribute_response = json.dumps(str(response))

    trace_id = uuid.uuid4().hex
    span_id = uuid.uuid4().hex[
        :16
    ]  # OTel span spec says it's only 8 bytes (16 hex chars), not 16 bytes.
    info = mlflow_entities.TraceInfo(
        request_id=trace_id,
        experiment_id=None,
        status=mlflow_entities.trace_status.TraceStatus.OK,
        timestamp_ms=time.time_ns() // 1_000_000,
        execution_time_ms=0,
        request_metadata=request_metadata,
    )
    span = mlflow_entities.Span(
        otel_span=OTelReadableSpan(
            name="root_span",
            context=build_otel_context(
                trace_id=decode_id(trace_id), span_id=decode_id(span_id)
            ),
            status=Status(StatusCode.OK),
            parent=None,
            attributes={
                mlflow_tracing_constant.SpanAttributeKey.REQUEST_ID: json.dumps(
                    trace_id
                ),
                mlflow_tracing_constant.SpanAttributeKey.INPUTS: attribute_request,
                mlflow_tracing_constant.SpanAttributeKey.OUTPUTS: attribute_response,
            },
        ),
    )

    data = mlflow_entities.TraceData(
        request=serialized_request, response=serialized_response, spans=[span]
    )
    trace = mlflow_entities.Trace(info=info, data=data)
    return trace


def create_minimal_error_trace(
    request: Dict[str, Any], response: Any
) -> mlflow_entities.Trace:
    """
    Create a minimal trace object with a single span, based on given request/response and error message.

    :param request: The request object. This is expected to be a JSON-serializable object
    :param response: The response object. This is expected to be a JSON-serializable object, but we cannot guarantee this
    :return: A new trace object.
    """
    trace = create_minimal_trace(request, response)
    trace.info.status = mlflow_entities.trace_status.TraceStatus.ERROR
    return trace


def inject_experiment_run_id_to_trace(
    trace: mlflow_entities.Trace, experiment_id: str, run_id: str
) -> mlflow_entities.Trace:
    """
    Inject the experiment and run ID into the trace metadata.

    :param trace: The trace object
    :param experiment_id: The experiment ID to inject
    :param run_id: The run ID to inject
    :return: The updated trace object
    """
    if trace.info.request_metadata is None:
        trace.info.request_metadata = {}
    trace.info.request_metadata[mlflow_tracing_constant.TraceMetadataKey.SOURCE_RUN] = (
        run_id
    )
    trace.info.experiment_id = experiment_id
    return trace


def update_trace_id(
    trace: mlflow_entities.Trace, new_trace_id: str
) -> mlflow_entities.Trace:
    """
    Helper method to update the trace ID of a trace object. This method updates both the TraceInfo
    as well as the trace ID of all spans in the trace.

    :param trace: The trace object
    :param new_trace_id: The new trace ID
    :return: The updated trace object
    """
    trace.info.request_id = new_trace_id
    trace.data.spans = [
        mlflow_entities.LiveSpan.from_immutable_span(
            span, span.parent_id, new_trace_id, new_trace_id
        ).to_immutable_span()
        for span in trace.data.spans
    ]
    return trace


def clone_trace_to_reupload(trace: mlflow_entities.Trace) -> mlflow_entities.Trace:
    """
    Prepare a trace for cloning by resetting traceId and clearing various fields.
    This has the downstream effect of causing the trace to be recreated with a new trace_id.

    :param trace: The trace to prepare
    :return: The prepared trace
    """
    prepared_trace = mlflow_entities.Trace.from_dict(trace.to_dict())

    # Since the semantics of this operation are to _clone_ the trace, and assessments are tied to
    # a specific trace, we clear assessments as well.
    prepared_trace.info.assessments = []

    # Tags and metadata also contain references to the source run, trace data artifact location, etc.
    # We clear these as well to ensure that the trace is not tied to the original source of the trace.
    for key in [k for k in prepared_trace.info.tags.keys() if k.startswith("mlflow.")]:
        prepared_trace.info.tags.pop(key)
    for key in [
        k
        for k in prepared_trace.info.request_metadata.keys()
        if k.startswith("mlflow.")
        and k
        not in [
            mlflow_tracing_constant.TraceMetadataKey.INPUTS,
            mlflow_tracing_constant.TraceMetadataKey.OUTPUTS,
        ]
    ]:
        prepared_trace.info.request_metadata.pop(key)

    return update_trace_id(prepared_trace, uuid.uuid4().hex)


# ================== Helper functions ==================
def _get_leaf_spans(trace: mlflow_entities.Trace) -> List[mlflow_entities.Span]:
    """Get all leaf spans in the trace."""
    if trace.data is None:
        return []
    spans = trace.data.spans or []
    leaf_spans_by_id = {span.span_id: span for span in spans}
    for span in spans:
        if span.parent_id:
            leaf_spans_by_id.pop(span.parent_id, None)
    return list(leaf_spans_by_id.values())


def _get_root_span(trace: mlflow_entities.Trace) -> Optional[mlflow_entities.Span]:
    """Get the root span in the trace."""
    if trace.data is None:
        return None
    spans = trace.data.spans or []
    # Root span is the span that has no parent
    return next((span for span in spans if span.parent_id is None), None)
