from concurrent.futures import ThreadPoolExecutor, as_completed

import logging
from typing import Optional, List

from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.paula_records.models import PAULARecord
from t_reporting_sdk.repositories.agent_runs.repository import AgentRunsRepository
from t_reporting_sdk.repositories.paula_records.repository import PAULARecordsRepository


def _load_default_paula_records_repository() -> PAULARecordsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_paula_records_repository
    return default_paula_records_repository


def _load_default_agent_runs_repository() -> AgentRunsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_agent_runs_repository
    return default_agent_runs_repository


class PAULAReporter:
    def __init__(
        self,
        agent_run: AgentRun,
        paula_repository: Optional[PAULARecordsRepository] = None,
        agent_runs_repository: Optional[AgentRunsRepository] = None,
    ):
        # Load default repositories if none are provided
        self._paula_repository = paula_repository or _load_default_paula_records_repository()
        agent_runs_repository = agent_runs_repository or _load_default_agent_runs_repository()

        self._agent_run = agent_run

        # Ensure Agent Run is stored in the database so that we can associate EVA results with it
        agent_runs_repository.store_agent_run(agent_run=agent_run)

    def report_paula_records(
        self,
        paula_records: List[PAULARecord],
        # Limit the # of saves made parallel - saves will fail if # of parallel calls > connection_pool size
        max_records_to_store_in_parallel: int = 4,
    ):
        def store_record(paula_record: PAULARecord):
            from requests.exceptions import HTTPError
            try:
                self._paula_repository.store_paula_record(
                    agent_run=self._agent_run,
                    paula_record=paula_record,
                )
            except HTTPError as e:
                logging.warning(
                    f"Failed to report PAULA record due to HTTP error: {e}; {e.response.text}"
                )
            except Exception as e:
                logging.exception("Failed to store record")
                logging.error(f"Unable to report prior authorization result: {e}")

        with ThreadPoolExecutor(max_workers=max_records_to_store_in_parallel) as executor:
            futures = {executor.submit(store_record, record): record for record in paula_records}

            for future in as_completed(futures):
                record = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Failed to process record: {record}: {e}")
