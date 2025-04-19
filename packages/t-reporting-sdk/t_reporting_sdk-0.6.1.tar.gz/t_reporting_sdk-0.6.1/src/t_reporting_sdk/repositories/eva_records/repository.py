from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.eva_records.models import EVARecord
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class EVARecordsRepository:
    def __init__(self, client: FabricClient):
        self._client = client

    def store_eva_record(
            self,
            agent_run: AgentRun,  # AgentRun to associate the EVARecord with
            eva_record: EVARecord,
    ) -> None:
        self._client.create_eva_record(
            run_id=agent_run.run_id,
            status=eva_record.status.value,
            exception_type=None if eva_record.exception_type is None else eva_record.exception_type.value,
            message=eva_record.message,
            customer_id=eva_record.customer_id,
            patient_id=eva_record.patient_id,
            payer_id=eva_record.payer_id,
            payer_name=eva_record.payer_name,
            portal=eva_record.portal,
            insurance_eligibility=None if eva_record.insurance_eligibility is None else eva_record.insurance_eligibility.value,
            insurance_type=None if eva_record.insurance_type is None else eva_record.insurance_type.value,
        )
