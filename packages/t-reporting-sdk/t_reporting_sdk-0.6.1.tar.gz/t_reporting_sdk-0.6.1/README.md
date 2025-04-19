# Reporting SDK

The Reporting SDK is a lightweight SDK utilized by ThoughtfulAI agents to report information about the individual 
units of execution an Agent performs. 

For example, in the context of EVA, an individual unit would be "Was the Patient eligible for the Payer given 
the patient history & insurance".

## Usage
```python
from t_reporting_sdk.domain.agent_runs.models import AgentRun
from t_reporting_sdk.domain.eva_records.models import EVAExceptionType, EVARecordStatus, EVARecord
from t_reporting_sdk.sdk.eva.eva_reporter import EVAReporter 

agent_run = AgentRun(
    run_id=123456,
)
eva_reporter = EVAReporter(agent_run=agent_run)

eva_records = [
    EVARecord(
        status=EVARecordStatus.ERROR,
        exception_type=EVAExceptionType.PATIENT_IDENTIFICATION,
        message="Multiple Patients Found in Cigna Payer search",
        customer_id="8463518",
        patient_id="P21546",
        payer_id="AA123456",
        portal="myAvatar",
    ),
    EVARecord(
        status=EVARecordStatus.ERROR,
        exception_type=EVAExceptionType.PATIENT_IDENTIFICATION,
        message="No patient found on Noridian Website",
        customer_id="8463518",
        patient_id="P997682",
        payer_id="AA123456",
        portal="Noridian",
    ),
]
eva_reporter.report_eva_records(eva_records=eva_records)
```

## Local Setup

### Setup virtual environment
There are many ways to approach this, so feel free to use your own flavor.

`python3.9 -m venv .venv`

### Activate virtual environment
`source .venv/bin/activate`

### Install dependencies
`pip install -r requirements-test.txt`

### Setup environment variables
#### Fabric Client
- `FABRIC_USER_EMAIL`  
  - Example: `blake.debenon@thoughtful.ai`
- `FABRIC_USER_OTP_SECRET`
  - The OTP secret is unique to each user and is stored in the database, encrypted with a dedicated KMS key
- `FABRIC_BASE_URL`
  - Example: `https://fabric.thoughtful-dev.ai`

## Running tests
From the source directory, run the following 

### Run unit tests
```shell
make test-unit
```

### Run integration tests
```shell
make test-integration
```

### Run all tests
```shell
make test-all
```
