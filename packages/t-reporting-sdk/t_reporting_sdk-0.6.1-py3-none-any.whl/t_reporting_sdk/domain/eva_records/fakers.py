from random import randint
from typing import Optional

from faker import Faker

from t_reporting_sdk.domain.eva_records.models import EVARecord, EVARecordStatus, EVAExceptionType, EVAInsuranceEligibility, EVAInsuranceType


class EVARecordFaker:
    @staticmethod
    def provide(
        status: Optional[EVARecordStatus] = None,
        exception_type: Optional[str] = None,
        message: Optional[str] = None,
        customer_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        payer_id: Optional[str] = None,
        payer_name: Optional[str] = None,
        portal: Optional[str] = None,
        insurance_eligibility: Optional[EVAInsuranceEligibility] = None,
        insurance_type: Optional[str] = None,
    ) -> EVARecord:
        faker = Faker()
        
        fake_status = EVARecordStatus.ERROR
        fake_exception_type = EVAExceptionType.MAPPING_FILE
        fake_message = faker.text(max_nb_chars=500)
        fake_customer_id = str(randint(1, 100))
        fake_patient_id = str(randint(1, 100))
        fake_payer_id = str(randint(1, 100))
        fake_payer_name = faker.company()
        fake_portal = faker.company()
        fake_insurance_eligibility = EVAInsuranceEligibility.ELIGIBLE
        fake_insurance_type = EVAInsuranceType.PRIMARY

        return EVARecord(
            status=status or fake_status,
            exception_type=exception_type or fake_exception_type,
            message=message or fake_message,
            customer_id=customer_id or fake_customer_id,
            patient_id=patient_id or fake_patient_id,
            payer_id=payer_id or fake_payer_id,
            payer_name=payer_name or fake_payer_name,
            portal=portal or fake_portal,
            insurance_eligibility=insurance_eligibility or fake_insurance_eligibility,
            insurance_type=insurance_type or fake_insurance_type,
        )
