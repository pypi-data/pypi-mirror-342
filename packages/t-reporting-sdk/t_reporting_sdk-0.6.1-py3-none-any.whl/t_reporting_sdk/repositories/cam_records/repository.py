from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.cam_records.models import CAMRecord
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class CAMRecordsRepository:
    def __init__(self, client: FabricClient):
        self._client = client

    def store_cam_record(
            self,
            agent_run: AgentRun,  # AgentRun to associate the CAMRecord with
            cam_record: CAMRecord,
    ) -> None:
        self._client.create_cam_record(
            run_id=agent_run.run_id,
            status=cam_record.status.value,
            exception_type=None if cam_record.exception_type is None else cam_record.exception_type.value,
            message=cam_record.message,
            customer_id=cam_record.customer_id,
            claim_id=cam_record.claim_id,
            work=cam_record.work,
            actioned=cam_record.actioned,
        ) 