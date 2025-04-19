import dataclasses
from typing import Optional

from dataclasses_json import dataclass_json

from databricks.rag_eval.monitoring import assessments, utils
from databricks.rag_eval.utils.enum_utils import StrEnum


class SchedulePauseStatus(StrEnum):
    UNPAUSED = "UNPAUSED"
    PAUSED = "PAUSED"


@dataclass_json
@dataclasses.dataclass
class MonitoringConfig:
    """
    Deprecated. Configuration for monitoring an GenAI application. All fields are optional for upsert semantics.
    """

    sample: Optional[float] = None
    metrics: Optional[list[str]] = None
    paused: Optional[bool] = None
    global_guidelines: Optional[dict[str, list[str]]] = None

    @classmethod
    def from_assessments_suite_config(
        cls, assessments_suite_config: assessments.AssessmentsSuiteConfig
    ) -> "MonitoringConfig":
        cfg = assessments_suite_config

        # metrics and guidelines uniqueness is enforced in AssessmentsSuiteConfig
        metrics: list[str] | None = None
        global_guidelines: dict[str, list[str]] | None = None

        if cfg.assessments is not None:
            metrics = []
            global_guidelines = {}

            for assessment in cfg.assessments:
                if isinstance(assessment, assessments.GuidelinesJudge):
                    metrics.append(assessments.AI_JUDGE_GUIDELINE_ADHERENCE)
                    global_guidelines = {
                        k: v.copy() for k, v in assessment.guidelines.items()
                    }

                if isinstance(assessment, assessments.BuiltinJudge):
                    metrics.append(str(assessment.name))

        return cls(
            sample=cfg.sample,
            paused=cfg.paused,
            metrics=metrics,
            global_guidelines=global_guidelines,
        )

    def to_assessments_suite_config(self) -> assessments.AssessmentsSuiteConfig:
        ls_assessments: list["assessments.AssessmentConfig"] | None = None

        if self.metrics is not None:
            ls_assessments = []
            for metric in self.metrics or []:
                if metric == assessments.AI_JUDGE_GUIDELINE_ADHERENCE:
                    ls_assessments.append(
                        assessments.GuidelinesJudge(
                            guidelines=(
                                {k: v.copy() for k, v in self.global_guidelines.items()}
                                if self.global_guidelines
                                else {}
                            )
                        )
                    )
                else:
                    ls_assessments.append(assessments.BuiltinJudge(name=metric))

        return assessments.AssessmentsSuiteConfig(
            sample=self.sample,
            paused=self.paused,
            assessments=ls_assessments,
        )


@dataclass_json
@dataclasses.dataclass
class Monitor:
    """
    The monitor for a serving endpoint.
    """

    endpoint_name: str
    evaluated_traces_table: str
    assessments_config: assessments.AssessmentsSuiteConfig
    experiment_id: str

    @property
    def monitoring_page_url(self) -> str:
        return utils.get_monitoring_page_url(self.experiment_id)


@dataclass_json
@dataclasses.dataclass
class ExternalMonitor:
    """
    The monitor for a GenAI application served outside of Databricks.
    """

    assessments_config: assessments.AssessmentsSuiteConfig
    _checkpoint_table: str
    experiment_id: str
    _legacy_ingestion_endpoint_name: str

    @property
    def monitoring_page_url(self) -> str:
        return utils.get_monitoring_page_url(self.experiment_id)
