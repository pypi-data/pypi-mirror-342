from concurrent.futures import ThreadPoolExecutor, as_completed

import logging
from typing import Optional, List

from requests import HTTPError

from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.eva_records.models import EVARecord
from t_reporting_sdk.repositories.agent_runs.repository import AgentRunsRepository
from t_reporting_sdk.repositories.eva_records.repository import EVARecordsRepository


def _load_default_eva_records_repository() -> EVARecordsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_eva_records_repository
    return default_eva_records_repository


def _load_default_agent_runs_repository() -> AgentRunsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_agent_runs_repository
    return default_agent_runs_repository


class EVAReporter:
    def __init__(
            self,
            agent_run: AgentRun,
            eva_repository: Optional[EVARecordsRepository] = None,
            agent_runs_repository: Optional[AgentRunsRepository] = None,
    ):
        # Load default repositories if none are provided
        self._eva_repository = _load_default_eva_records_repository() if eva_repository is None else eva_repository
        agent_runs_repository = _load_default_agent_runs_repository() if agent_runs_repository is None else agent_runs_repository

        self._agent_run = agent_run

        # Ensure Agent Run is stored in the database so that we can associate EVA results with it
        agent_runs_repository.store_agent_run(agent_run=agent_run)

    def report_eva_records(
            self,
            eva_records: List[EVARecord],
            # Limit the # of saves made parallel - saves will fail if # of parallel calls > connection_pool size
            max_records_to_store_in_parallel: int = 4,
    ):
        def store_record(eva_record: EVARecord):
            try:
                self._eva_repository.store_eva_record(
                    agent_run=self._agent_run,
                    eva_record=eva_record,
                )
            except HTTPError as e:
                logging.warning(f"Failed to report EVA record due to HTTP error: {e}; {e.response.text}")
            except Exception as e:
                logging.error(f"Unable to report eligibility verification result: {e}")

        with ThreadPoolExecutor(max_workers=max_records_to_store_in_parallel) as executor:
            futures = {executor.submit(store_record, record): record for record in eva_records}

            for future in as_completed(futures):
                record = futures[future]
                try:
                    future.result()  # Will raise an exception if the task failed
                except Exception as e:
                    logging.error(f"Failed to process record {record}: {e}")


class EvaReporter(EVAReporter):
    def __new__(cls, *args, **kwargs):
        logging.warning(f"{cls.__name__} is deprecated. Please use EVAReporter instead.")
        return super().__new__(cls)