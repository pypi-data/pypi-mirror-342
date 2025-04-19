from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EVARecordStatus(Enum):
    # Successfully conducted eligibility check. No issues/warnings encountered.
    SUCCESS = 'success'

    # Successfully conducted eligibility check but encountered a scenario that requires staff review.
    WARNING = 'warning'

    # Unable to conduct eligibility check
    ERROR = 'error'

    # Skipped typically indicates that the scenario is a known-out of scope scenario
    SKIPPED = 'skipped'


class EVAExceptionType(Enum):
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

    # Exceptions related to retrieving coverage details from external portals or payers.
    COVERAGE_RETRIEVAL = 'coverage_retrieval'

    # Exceptions related to retrieving payer details.
    NO_PAYER_FOUND = 'no_payer_found'

    # Situations involving multiple payers, extra COB info, or special secondary coverage complexities.
    MULTIPLE_PAYER_OR_COB = 'multiple_payer_or_cob'

    # Related to missing, invalid, or soon-to-expire plan effective/end dates.
    COVERAGE_DATE = 'coverage_date'

    # Copay-related issues, such as unusually large copays that require review.
    COPAY = 'copay'

    # Issues where the patient cannot be identified or matched in the system.
    PATIENT_IDENTIFICATION = 'patient_identification'

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


class EVAInsuranceEligibility(Enum):
    ELIGIBLE = 'eligible'
    INELIGIBLE = 'ineligible'


class EVAInsuranceType(Enum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    TERTIARY = 'tertiary'
    QUATERNARY = 'quaternary'


class EVARecord(BaseModel):
    status: EVARecordStatus
    exception_type: Optional[EVAExceptionType]
    message: str  # Additional context about the exception provided by the Agent.
    customer_id: str  # ID of the Thoughtful customer

    # EVA records typically refer to a patient/payer combo run on a specific portal
    patient_id: str  # ID of the patient eligibility verification is being performed on
    payer_id: Optional[str]   # ID of the Payer that eligibility verification is being checked against
    payer_name: Optional[str] = None # Name of the payer that eligibility verification is being checked against
    portal: str  # Name of the portal being interacted with
    insurance_eligibility: Optional[EVAInsuranceEligibility] = None # Insurance eligibility status of the patient
    insurance_type: Optional[EVAInsuranceType] = None  # Type of insurance (primary, secondary, etc.)
