from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator


class PAULARecordStatus(Enum):
    # There was an exception or other error during the run
    ERROR = 'error'
    
    # We are skipping over authorization for this payer due to out of scope of automation or integration not yet implemented
    SKIPPED = 'skipped'
    
    # The authorization is still being reviewed
    PENDING = 'pending'
    
    # The authorization has been reviewed and was approved
    APPROVED = 'approved'
    
    # The authorization has been reviewed and was denied
    DENIED = 'denied'
    
    # The authorization is not required for the payer after the auth submission process
    NO_AUTH_REQUIRED = 'no_auth_required'


class PAULAExceptionType(Enum):
    """
    Exception type specified by the Agent. These categories are designed to be general enough to apply
    to various customers, payers, and portals.
    """

    # Related to missing information in the mapping file (e.g., payer not found in mapping file).
    MAPPING_FILE = 'mapping_file'

    # Related incomplete or invalid patient demographic data (e.g., missing gender or invalid zip code).
    PATIENT_DEMOGRAPHIC = 'patient_demographic'

    # Discrepancy where a patient’s name does not match between different systems (e.g., Valant vs. Availity).
    PATIENT_NAME_MISMATCH = 'patient_name_mismatch'

    # Exceptions related to retrieving payer details.
    NO_PAYER_FOUND = 'no_payer_found'

    # Situations involving multiple payers, extra COB info, or special secondary coverage complexities.
    MULTIPLE_PAYER_OR_COB = 'multiple_payer_or_cob'

    # Related to missing, invalid, or soon-to-expire plan effective/end dates.
    COVERAGE_DATE = 'coverage_date'

    # Issues where the patient cannot be identified or matched in the system.
    PATIENT_IDENTIFICATION = 'patient_identification'
    
    # Providers often miss or assign outdated / invalid CPT code
    INVALID_CPT_CODE = "invalid_cpt_code" 

    # Diagnosis codes could be missing or invalid
    INVALID_ICD_CODE = "invalid_icd_code"

    # The provider may put a number of units that exceeds the patients allowable limit
    INVALID_UNITS = "invalid_units"

    # Claim had already been submitted / another claim with the same service and date of service already exists in the PMS.
    DUPLICATE_AUTHORIZATION = "duplicate_authorization"

    # Provider may not be registered under a particular payer. (Often occurs with Medicare)
    INVALID_PROVIDER_NPI = "invalid_provider_npi" 

    # Some claims require a referring provider
    MISSING_REFERRING_PROVIDER = "missing_referring_provider"
    
    # Exception for missing required info (e.g., chart notes, medical docs, pain level, etc.).
    MISSING_MEDICAL_DOCUMENTATION = "missing_medical_documentation"

    # HTTP or connectivity-related issues (e.g., 404 Not Found, 401 Unauthorized) when accessing external APIs.
    HTTP_CONNECTIVITY = 'http_connectivity'

    # Internal validation or formatting issues in data fields (e.g., length restrictions not met).
    VALIDATION_FORMAT = 'validation_format'

    # Related to technical issues indicating unexpected code-level issues.
    TECHNICAL_ATTRIBUTE = 'technical_attribute'

    # Exceptions that do not fit well into the other categories. Typically, customer specific.
    # Before classifying an exception as "CUSTOM", consider if we need to create a new ENUM type (the current list
    # is not exhaustive and will be expanded over time to include new exception types that are generalizable across
    # customers.
    CUSTOM = 'custom'

    # A catch-all for unexpected or generic exceptions not covered by other categories.
    UNEXPECTED = 'unexpected'


class PAULARecordOriginalStatus(Enum):
    # Indicates that the authorization record is a standard submission request for prior authorization.
    NONE = 'none'
    
    # Indicates that the authorization record is a follow-up check on a previously submitted prior authorization.
    PENDING = 'pending'


class PAULARecord(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    status: PAULARecordStatus
    exception_type: Optional[PAULAExceptionType]
    message: Optional[str] # Additional context about the exception provided by the Agent.
    customer_id: str # ID of Thoughtful customer

    original_status: PAULARecordOriginalStatus
    patient_id: str
    portal: str
    appointment_date: datetime
    treatment_code: str # HCPC, CPT, procedure
    payer: Optional[str] # required for PENDING, DENIED, APPROVED
    payer_id: Optional[str] # required for PENDING, DENIED, APPROVED
    plan_id: Optional[str] # Required if we have a payer/payer_id
    system_of_record_id: str # ID of the underyling system assoicated with the prior auth
    authorization_id: Optional[str] # required for DENIED, APPROVED. Refers to reference ID

    @field_validator('appointment_date', mode='before')
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError('appointment_date must be timezone-aware')
        return value.astimezone(timezone.utc)
    
    @field_validator('payer', 'payer_id', mode='before')
    @classmethod
    def ensure_payer(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data['status'] in [PAULARecordStatus.PENDING, PAULARecordStatus.DENIED, PAULARecordStatus.APPROVED]:
            if value is None:
                raise ValueError('payer and payer_id are required for PENDING, DENIED, and APPROVED status')
        return value
    
    @field_validator('plan_id', mode='before')
    @classmethod
    def ensure_plan_id(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data['payer'] is not None and value is None:
            raise ValueError('plan_id is required when payer is provided')
        return value
    
    @field_validator('authorization_id', mode='before')
    @classmethod
    def ensure_authorization_id(cls, value: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data['status'] in [PAULARecordStatus.DENIED, PAULARecordStatus.APPROVED]:
            if value is None:
                raise ValueError('authorization_id is required for DENIED and APPROVED status')
        return value
