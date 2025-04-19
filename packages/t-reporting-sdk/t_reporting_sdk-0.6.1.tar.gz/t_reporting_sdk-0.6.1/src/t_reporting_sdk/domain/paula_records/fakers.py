from datetime import datetime, timezone
from random import randint
from typing import Optional

from faker import Faker

from t_reporting_sdk.domain.paula_records.models import PAULARecord, PAULARecordStatus, PAULARecordOriginalStatus, PAULAExceptionType


class PAULARecordFaker:
    @staticmethod
    def provide(
        status: Optional[PAULARecordStatus] = None,
        exception_type: Optional[PAULAExceptionType] = None,
        message: Optional[str] = None,
        customer_id: Optional[str] = None,
        original_status: Optional[PAULARecordOriginalStatus] = None,
        patient_id: Optional[str] = None,
        portal: Optional[str] = None,
        appointment_date: Optional[datetime] = None,
        treatment_code: Optional[str] = None,
        payer: Optional[str] = None,
        payer_id: Optional[str] = None,
        plan_id: Optional[str] = None,
        system_of_record_id: Optional[str] = None,
        authorization_id: Optional[str] = None,
    ) -> PAULARecord:
        faker = Faker()

        fake_status = status or faker.enum(PAULARecordStatus)
        fake_exception_type = exception_type or (faker.enum(PAULAExceptionType) if fake_status == PAULARecordStatus.ERROR else None)
        fake_message = message or (faker.text(max_nb_chars=100) if fake_exception_type is not None else None)
        fake_customer_id = customer_id or str(randint(1, 100))
        fake_original_status = original_status or faker.enum(PAULARecordOriginalStatus)
        fake_patient_id = patient_id or str(randint(1, 100))
        fake_portal = portal or faker.company()
        fake_appointment_date = appointment_date or faker.date_time_this_month(tzinfo=timezone.utc)
        fake_treatment_code = treatment_code or faker.word()
        fake_payer = payer or (faker.company() if fake_status in [PAULARecordStatus.PENDING, PAULARecordStatus.DENIED, PAULARecordStatus.APPROVED] else None)
        fake_payer_id = payer_id or (str(randint(1, 100)) if fake_status in [PAULARecordStatus.PENDING, PAULARecordStatus.DENIED, PAULARecordStatus.APPROVED] else None)
        fake_plan_id = plan_id or (str(randint(1, 100)) if fake_payer is not None else None)
        fake_system_of_record_id = system_of_record_id or str(randint(1, 100))
        fake_authorization_id = authorization_id or (str(randint(1, 100)) if fake_status in [PAULARecordStatus.DENIED, PAULARecordStatus.APPROVED] else None)

        return PAULARecord(
            status=fake_status,
            exception_type=fake_exception_type,
            message=fake_message,
            customer_id=fake_customer_id,
            original_status=fake_original_status,
            patient_id=fake_patient_id,
            portal=fake_portal,
            appointment_date=fake_appointment_date,
            treatment_code=fake_treatment_code,
            payer=fake_payer,
            payer_id=fake_payer_id,
            plan_id=fake_plan_id,
            system_of_record_id=fake_system_of_record_id,
            authorization_id=fake_authorization_id,
        )