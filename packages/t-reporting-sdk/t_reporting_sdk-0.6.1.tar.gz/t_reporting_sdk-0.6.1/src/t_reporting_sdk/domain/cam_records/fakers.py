import random
from random import randint
from typing import Optional

from faker import Faker

from t_reporting_sdk.domain.cam_records.models import CAMRecord, CAMRecordStatus, CAMExceptionType


class CAMRecordFaker:
    """
    Generates fake CAMRecord objects for testing purposes.
    """

    @staticmethod
    def provide(
            status: Optional[CAMRecordStatus] = None,
            exception_type: Optional[CAMExceptionType] = None,
            message: Optional[str] = None,
            customer_id: Optional[str] = None,
            claim_id: Optional[str] = None,
            work: Optional[str] = None,
            actioned: Optional[bool] = None,
    ) -> CAMRecord:
        """
        Provides a fake CAMRecord with the given parameters, or random values if not provided.
        """
        faker = Faker()
        
        fake_status = random.choice(list(CAMRecordStatus))
        fake_exception_type = random.choice(list(CAMExceptionType)) if fake_status in [CAMRecordStatus.ERROR, CAMRecordStatus.WARNING] else None
        
        if fake_exception_type is not None:
            fake_message = f"Encountered {fake_exception_type.value} issue: {faker.sentence()}"
        else:
            fake_message = faker.sentence() if fake_status != CAMRecordStatus.SUCCESS else ""
            
        fake_customer_id = str(randint(1, 100))
        fake_claim_id = str(randint(1, 100))
        fake_work = faker.word()
        fake_actioned = random.choice([True, False])
        
        # If status is not ERROR or WARNING, exception_type should be None
        if status is not None and status not in [CAMRecordStatus.ERROR, CAMRecordStatus.WARNING]:
            exception_type = None

        return CAMRecord(
            status=status or fake_status,
            exception_type=exception_type or fake_exception_type,
            message=message or fake_message,
            customer_id=customer_id or fake_customer_id,
            claim_id=claim_id or fake_claim_id,
            work=work or fake_work,
            actioned=actioned or fake_actioned,
        ) 