from typing import Optional, List
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from requests import HTTPError

from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.cam_records.models import CAMRecord
from t_reporting_sdk.repositories.agent_runs.repository import AgentRunsRepository
from t_reporting_sdk.repositories.cam_records.repository import CAMRecordsRepository


def _load_default_cam_records_repository() -> CAMRecordsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_cam_records_repository
    return default_cam_records_repository


def _load_default_agent_runs_repository() -> AgentRunsRepository:
    """
    Handles dependency injection automatically so that SDK users do not have to specify their dependencies manually.
    Handled as a separate function so that tests do not try to import the default repositories
    """
    from t_reporting_sdk.default_dependencies import default_agent_runs_repository
    return default_agent_runs_repository


class CAMReporter:
    def __init__(
            self,
            agent_run: AgentRun,
            cam_repository: Optional[CAMRecordsRepository] = None,
            agent_runs_repository: Optional[AgentRunsRepository] = None,
    ):
        # Load default repositories if none are provided
        self._cam_repository = _load_default_cam_records_repository() if cam_repository is None else cam_repository
        agent_runs_repository = _load_default_agent_runs_repository() if agent_runs_repository is None else agent_runs_repository

        self._agent_run = agent_run

        # Ensure Agent Run is stored in the database so that we can associate CAM results with it
        agent_runs_repository.store_agent_run(agent_run=agent_run)

    def report_cam_records(
            self,
            cam_records: List[CAMRecord],
            # Limit the # of saves made parallel - saves will fail if # of parallel calls > connection_pool size
            max_records_to_store_in_parallel: int = 4,
    ) -> None:
        def store_record(cam_record: CAMRecord) -> None:
            try:
                self._cam_repository.store_cam_record(
                    agent_run=self._agent_run,
                    cam_record=cam_record,
                )
            except HTTPError as e:
                logging.warning(
                    f"Failed to report EVA record due to HTTP error: {e}; {e.response.text}"
                )
            except Exception as e:
                logging.error(f"Unable to report CAM result: {e}")

        with ThreadPoolExecutor(max_workers=max_records_to_store_in_parallel) as executor:
            futures = {executor.submit(store_record, record): record for record in cam_records}

            for future in as_completed(futures):
                record = futures[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Failed to process record {record}: {e}")