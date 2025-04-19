"""
Introduces main Context class and the framework to specify different specialized
contexts.
"""

from __future__ import annotations

import functools
import logging
import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

import mlflow

from databricks.rag_eval import session

if TYPE_CHECKING:
    from databricks.rag_eval.clients import managed_evals_client, managed_rag_client
_logger = logging.getLogger(__name__)


class Context(ABC):
    """
    Abstract class for execution context.
    Context is stateless and should NOT be used to store information related to specific eval run.
    """

    @abstractmethod
    def display_html(self, html: str) -> None:
        """
        Displays HTML in the current execution context.
        """
        pass

    @abstractmethod
    def build_managed_rag_client(self) -> "managed_rag_client.ManagedRagClient":
        """
        Build a LLM Judge client for the current eval session.
        """
        pass

    @abstractmethod
    def build_managed_evals_client(self) -> "managed_evals_client.ManagedEvalsClient":
        """
        Build a Managed Evals client for the current eval session.
        """
        pass

    @abstractmethod
    def get_job_id(self) -> Optional[str]:
        """
        Get the current job ID.
        """
        pass

    @abstractmethod
    def get_job_run_id(self) -> Optional[str]:
        """
        Get the current job run ID.
        """
        pass

    @abstractmethod
    def get_mlflow_run_id(self) -> Optional[str]:
        """
        Gets the MLflow RunId, or None if not running within an MLflow run.
        """
        pass

    @abstractmethod
    def get_user_name(self) -> Optional[str]:
        """
        Get the current user's name.
        """
        pass


class NoneContext(Context):
    """
    A context that does nothing.
    """

    def display_html(self, html: str) -> None:
        raise AssertionError("Context is not set")

    def build_managed_rag_client(self) -> "managed_rag_client.ManagedRagClient":
        raise AssertionError("Context is not set")

    def build_managed_evals_client(self) -> "managed_evals_client.ManagedEvalsClient":
        raise AssertionError("Context is not set")

    def get_job_id(self) -> Optional[str]:
        raise AssertionError("Context is not set")

    def get_job_run_id(self) -> Optional[str]:
        raise AssertionError("Context is not set")

    def get_mlflow_run_id(self) -> Optional[str]:
        raise AssertionError("Context is not set")

    def get_user_name(self) -> Optional[str]:
        raise AssertionError("Context is not set")


class RealContext(Context):
    """
    Context for eval execution.

    NOTE: This class is not covered by unit tests and is meant to be tested through
    smoke tests that run this code on an actual Databricks cluster.
    """

    @classmethod
    def _get_dbutils(cls):
        """
        Returns an instance of dbutils.
        """
        try:
            from databricks.sdk.runtime import dbutils

            return dbutils
        except ImportError:
            import IPython

            dbutils = IPython.get_ipython().user_ns["dbutils"]
        return dbutils

    def __init__(self):
        self._dbutils = self._get_dbutils()
        try:
            self._notebook_context = (
                self._dbutils.entry_point.getDbutils().notebook().getContext()
            )
        except Exception:
            self._notebook_context = None

        # Set MLflow model registry to Unity Catalog
        mlflow.set_registry_uri("databricks-uc")

    def display_html(self, html) -> None:
        # pylint: disable=protected-access
        self._dbutils.notebook.displayHTML(html)

    def build_managed_rag_client(self) -> "managed_rag_client.ManagedRagClient":
        from databricks.rag_eval.clients.managedrag import managed_rag_client

        return managed_rag_client.ManagedRagClient()

    def build_managed_evals_client(self) -> "managed_evals_client.ManagedEvalsClient":
        from databricks.rag_eval.clients.managedevals import managed_evals_client

        return managed_evals_client.ManagedEvalsClient()

    def get_job_id(self) -> Optional[str]:
        try:
            return self._notebook_context.jobId().get()
        except Exception:
            return None

    def get_job_run_id(self) -> Optional[str]:
        try:
            return self._notebook_context.parentRunId().get()
        except Exception:
            return None

    def get_mlflow_run_id(self) -> Optional[str]:
        if mlflow.active_run():
            return mlflow.active_run().info.run_id

    def get_user_name(self) -> Optional[str]:
        try:
            return self._notebook_context.userName().get()
        except Exception:
            return None


# Context is a singleton.
_context_singleton = NoneContext()


def context_is_active() -> bool:
    """
    Check if a context is active.
    """
    return not isinstance(get_context(), NoneContext)


def get_context() -> Context:
    """
    Get the context.
    """
    return _context_singleton or NoneContext()


def eval_context(func):
    """
    Decorator for wrapping all eval APIs with setup and closure logic.

    Sets up a context singleton with RealContext if there isn't one already.
    Initializes the session for the current thread. Clears the session after the function is executed.

    :param func: eval function to wrap
    :return: return value of func
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Set up the context singleton if it doesn't exist
        if not context_is_active():
            global _context_singleton
            _context_singleton = RealContext()

        if session.current_session() is None:
            # Initialize the session
            session.init_session(str(uuid.uuid4()))
            root_call = True
        else:
            root_call = False

        error = None
        result = None

        try:
            result = func(*args, **kwargs)
        except Exception as e:  # pylint: disable=broad-except
            error = e
        finally:
            # Clear the session if this is a root call
            if root_call:
                session.clear_session()
            # Raise the original error if there was one, otherwise return
            if error is not None:
                raise error
            else:
                return result  # pylint: disable=lost-exception

    return wrapper
