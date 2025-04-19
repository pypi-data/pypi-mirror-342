from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class AgentRunsRepository:
    def __init__(self, client: FabricClient):
        self._client = client

    def store_agent_run(
            self,
            agent_run: AgentRun,
    ) -> None:
        self._client.create_agent_run(run_id=agent_run.run_id, run_date=agent_run.run_date)
