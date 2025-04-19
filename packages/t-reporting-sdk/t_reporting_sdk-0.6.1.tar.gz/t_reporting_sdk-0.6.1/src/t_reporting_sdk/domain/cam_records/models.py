from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CAMRecordStatus(Enum):
    # Successfully processed entire claim. No issues/warnings encountered.
    SUCCESS = 'success'

    # Successfully processed claim but encountered a scenario that requires staff review.
    WARNING = 'warning'

    # Unable to process claim
    ERROR = 'error'

    # Skipped typically indicates that the scenario is a known-out of scope scenario
    SKIPPED = 'skipped'


class CAMExceptionType(Enum):
    """
    Exception type specified by the Agent. These categories are designed to be general enough to apply
    to various customers, payers, and claim processing scenarios.
    """
    # CAMs often run after EVAs, and some records might have failed processing at the eligibility level, perhaps missing benefits too.
    MISSING_ELIGIBILITY_OR_BENEFITS_INFO = 'missing_eligibility_or_benefits_info'
    
    # Related to missing information in the mapping file/store (e.g., value to correct is not listed in mapping).
    MAPPING_MISSING_OR_INCORRECT = 'mapping'
    
    # The claim to process for CAM was not in the right status, perhaps it was put on the queue in error.
    IMPROPER_STATUS = "improper_status"
    
    # An RPA error was encountered, could be a missing locator or some other RPA/browser related issue.
    RPA_ERROR = "rpa_error"
    
    # For desktop applications, when an error was encountered due to a missing locator, or someone else using the app (if the app is single user concurrently).
    DEKSTOP_ERROR = "desktop_error"
    
    # Something with a private API (i.e. not publicly documented) went wrong.
    PRIVATE_API = "private_api"
    
    # A file needed to complete the processing of a claim is missing, perhaps a file we/our customers are responsible for, or even an attachment like an x-ray or receipt.
    MISSING_REQUIRED_FILE = "missing_required_file"
    
    # Providers often miss or assign outdated / invalid CPT or diagnosis code
    INVALID_CPT_OR_ICD_CODE = "invalid_cpt_or_icd_code" 
    
    # Something about the state of the claim is wrong, like missing a modifier, missing a referring provider, missing a location associated or invalid units.
    IMPROPER_CLAIM_STATE = "improper_claim_state"

    # Claim had already been submitted / another claim with the same service and date of service already exists in the PMS.
    DUPLICATE_CLAIM = "duplicate_claim"

    # Provider may not be registered under a particular payer. (Often occurs with Medicare)
    INVALID_PROVIDER_NPI = "invalid_provider_npi" 
    
    # Related incomplete or invalid patient demographic data (e.g., missing gender or invalid zip code).
    PATIENT_DEMOGRAPHIC = 'patient_demographic'

    # Discrepancy where a patient's name does not match between different systems (e.g., Valant vs. Availity).
    PATIENT_NAME_MISMATCH = 'patient_name_mismatch'
    
    # Issues where the patient cannot be identified or matched in the system.
    PATIENT_IDENTIFICATION = 'patient_identification'
    
    # HTTP or connectivity-related issues (e.g., 404 Not Found, 401 Unauthorized) when accessing external APIs.
    HTTP_CONNECTIVITY = 'http_connectivity'
    
    # Internal validation or formatting issues in data fields (e.g., length restrictions not met).
    VALIDATION_FORMAT = 'validation_format'
    
    # Exceptions that do not fit well into the other categories. Typically, customer specific.
    # Before classifying an exception as "CUSTOM", consider if we need to create a new ENUM type (the current list
    # is not exhaustive and will be expanded over time to include new exception types that are generalizable across
    # customers.
    CUSTOM = 'custom'

    # A catch-all for unexpected or generic exceptions not covered by other categories.
    UNEXPECTED = 'unexpected'


class CAMRecord(BaseModel):
    status: CAMRecordStatus
    exception_type: Optional[CAMExceptionType]
    message: Optional[str]  # Additional context about the exception provided by the Agent.
    customer_id: str  # ID of Thoughtful customer
    claim_id: str  # ID of the claim being performed on
    work: str  # the work performed relating to the claim
    actioned: bool  # Whether the CAM agent did anything to the record at all, useful for CAMs where it is checking, and non-action is the ideal outcome 