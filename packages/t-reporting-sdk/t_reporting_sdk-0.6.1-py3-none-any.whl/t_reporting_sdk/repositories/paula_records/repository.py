from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.paula_records.models import PAULARecord
from t_reporting_sdk.repositories.api_clients.fabric.client import FabricClient


class PAULARecordsRepository:
    def __init__(self, client: FabricClient):
        self._client = client

    def store_paula_record(
        self,
        agent_run: AgentRun,  # AgentRun to associate the PAULARecord with
        paula_record: PAULARecord,
    ) -> None:
        self._client.create_paula_record(
            run_id=agent_run.run_id,
            status=paula_record.status.value,
            exception_type=None if paula_record.exception_type is None else paula_record.exception_type.value,
            message=paula_record.message,
            customer_id=paula_record.customer_id,
            original_status=None if paula_record.original_status is None else paula_record.original_status.value,
            patient_id=paula_record.patient_id,
            portal=paula_record.portal,
            appointment_date=paula_record.appointment_date.isoformat(),
            treatment_code=paula_record.treatment_code,
            payer=paula_record.payer,
            payer_id=paula_record.payer_id,
            plan_id=paula_record.plan_id,
            system_of_record_id=paula_record.system_of_record_id,
            authorization_id=paula_record.authorization_id,
        )
