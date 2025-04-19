"""REST API entities for monitoring."""

import dataclasses
from typing import Literal, Optional

from dataclasses_json import config, dataclass_json

from databricks.rag_eval.monitoring import assessments, entities

_FIELD_IS_UPDATABLE = "FIELD_IS_UPDATABLE"


def ExcludeIfNone(value):
    return value is None


@dataclass_json
@dataclasses.dataclass
class AssessmentConfig:
    name: Optional[str] = None
    sample_rate: Optional[float] = dataclasses.field(
        default=None,
        metadata=config(exclude=ExcludeIfNone),
    )


@dataclass_json
@dataclasses.dataclass
class NamedGuidelineEntry:
    key: Optional[str] = None
    guidelines: Optional[list[str]] = None


@dataclass_json
@dataclasses.dataclass
class NamedGuidelines:
    entries: Optional[list[NamedGuidelineEntry]]


@dataclass_json
@dataclasses.dataclass
class EvaluationConfig:
    metrics: Optional[list[AssessmentConfig]] = None
    no_metrics: Optional[bool] = None
    named_guidelines: Optional[NamedGuidelines] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )


@dataclass_json
@dataclasses.dataclass
class SamplingConfig:
    sampling_rate: Optional[float] = None


@dataclass_json
@dataclasses.dataclass
class ScheduleConfig:
    pause_status: Optional[Literal["UNPAUSED", "PAUSED"]] = None


@dataclass_json
@dataclasses.dataclass
class Monitor:
    experiment_id: Optional[str] = dataclasses.field(
        default=None,
        metadata={**config(exclude=ExcludeIfNone), _FIELD_IS_UPDATABLE: False},
    )
    evaluation_config: Optional[EvaluationConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )
    sampling: Optional[SamplingConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )
    schedule: Optional[ScheduleConfig] = dataclasses.field(
        default=None, metadata=config(exclude=ExcludeIfNone)
    )
    is_agent_external: Optional[bool] = dataclasses.field(
        default=None,
        metadata={**config(exclude=ExcludeIfNone), _FIELD_IS_UPDATABLE: False},
    )
    evaluated_traces_table: Optional[str] = dataclasses.field(
        default=None,
        metadata={**config(exclude=ExcludeIfNone), _FIELD_IS_UPDATABLE: False},
    )

    def get_update_mask(self) -> str:
        """Get the update mask for the fields that have changed."""
        return ",".join(
            field.name
            for field in dataclasses.fields(self)
            if getattr(self, field.name) is not None
            and field.metadata.get(_FIELD_IS_UPDATABLE, True)
        )


@dataclass_json
@dataclasses.dataclass
class MonitorInfo:
    monitor: Optional[Monitor] = None
    endpoint_name: Optional[str] = None

    @property
    def is_external(self) -> bool:
        """Returns True if the monitor is external."""
        return self.monitor and self.monitor.is_agent_external

    def _get_assessments_suite_config(self) -> assessments.AssessmentsSuiteConfig:
        """Extract common monitoring configuration logic."""
        monitor = self.monitor or Monitor()
        sampling_config = monitor.sampling or SamplingConfig()
        evaluation_config = monitor.evaluation_config or EvaluationConfig()
        assessment_configs = evaluation_config.metrics or []

        # Convert named guidelines
        global_guidelines = None
        if (
            monitor.evaluation_config
            and monitor.evaluation_config.named_guidelines
            and monitor.evaluation_config.named_guidelines.entries
        ):
            global_guidelines = {
                entry.key: entry.guidelines
                for entry in monitor.evaluation_config.named_guidelines.entries
                if entry.key and entry.guidelines
            }

        pause_status = monitor.schedule.pause_status if monitor.schedule else None

        judges = []
        for cfg in assessment_configs:
            if cfg.name != assessments.AI_JUDGE_GUIDELINE_ADHERENCE:
                judges.append(
                    assessments.BuiltinJudge(name=cfg.name, sample_rate=cfg.sample_rate)
                )
            # Note that we do not create a GuidelinesJudge if the guidelines are empty,
            # even if `guideline_adherence` is included in assessment configs from the server.
            # This is because having a GuidelinesJudge without guidelines doesn't make sense.
            elif (
                cfg.name == assessments.AI_JUDGE_GUIDELINE_ADHERENCE
                and global_guidelines
            ):
                judges.append(
                    assessments.GuidelinesJudge(
                        guidelines=global_guidelines,
                        sample_rate=cfg.sample_rate,
                    )
                )

        return assessments.AssessmentsSuiteConfig(
            sample=sampling_config.sampling_rate,
            paused=pause_status == entities.SchedulePauseStatus.PAUSED,
            assessments=judges,
        )

    def to_monitor(self) -> entities.Monitor:
        """Converts the REST API response to a Python Monitor object."""
        monitor = self.monitor or Monitor()
        assert not monitor.is_agent_external, "Monitor is external"

        return entities.Monitor(
            endpoint_name=self.endpoint_name,
            evaluated_traces_table=monitor.evaluated_traces_table,
            experiment_id=monitor.experiment_id,
            assessments_config=self._get_assessments_suite_config(),
        )

    def to_external_monitor(self) -> entities.ExternalMonitor:
        """Converts the REST API response to an External Monitor object."""
        monitor = self.monitor or Monitor()
        assert monitor.is_agent_external, "Monitor is internal"

        return entities.ExternalMonitor(
            assessments_config=self._get_assessments_suite_config(),
            _checkpoint_table=monitor.evaluated_traces_table,
            experiment_id=monitor.experiment_id,
            _legacy_ingestion_endpoint_name=self.endpoint_name,
        )


@dataclass_json
@dataclasses.dataclass
class JobCompletionEvent:
    success: Optional[bool] = None
    error_message: Optional[str] = None


@dataclass_json
@dataclasses.dataclass
class MonitoringEvent:
    job_start: Optional[dict] = None
    job_completion: Optional[JobCompletionEvent] = None


@dataclasses.dataclass
class MonitoringMetric:
    num_traces: Optional[int] = None
    num_traces_evaluated: Optional[int] = None

    def to_dict(self) -> dict:
        output_dict = {}
        if self.num_traces is not None:
            output_dict["num_traces"] = self.num_traces

        if self.num_traces_evaluated is not None:
            output_dict["num_traces_evaluated"] = self.num_traces_evaluated
        return output_dict
