# Parcha API Client

A Python client for interacting with the [Parcha API](https://docs.parcha.ai), providing both synchronous and asynchronous methods for Know Your Business (KYB) and Know Your Customer (KYC) verifications. This client makes it easy to integrate Parcha's powerful verification services into your Python applications.

## 🌟 Features

- **KYB (Know Your Business) Verification**
  - Start and manage KYB verification jobs
  - Customizable business verification schemas
  - Parallel check execution support

- **KYC (Know Your Customer) Verification**
  - Start and manage KYC verification jobs
  - Flexible customer verification schemas
  - Support for multiple verification checks

- **Job Management**
  - Track verification progress
  - Retrieve job results
  - Get job status updates

- **Modern Python Features**
  - Both synchronous and asynchronous APIs
  - Type hints for better IDE support
  - Pydantic models for request/response validation

- **Integration Options**
  - Webhook support for job status updates
  - Slack notifications
  - Customizable run configurations

## 🚀 Installation

```bash
pip install parcha-api
```

## 📖 Quick Start

```python
from parcha_api import ParchaAPI, KYBAgentJobInput

# Initialize the client
api = ParchaAPI(
    base_url="https://api.parcha.ai",
    token="your_api_token"  # Get this from your Parcha dashboard
)

# Start a KYB verification
kyb_input = KYBAgentJobInput(
    agent_key="your_agent_key",
    kyb_schema={
        "business_name": "Acme Corp",
        "registration_number": "12345678",
        "country": "US"
    },
    webhook_url="https://your-webhook.com/callback",  # Optional
    run_in_parallel=True  # Optional: Run checks in parallel
)

# Synchronous usage
response = api.start_kyb_agent_job(kyb_input)
print(f"Job started with ID: {response['job_id']}")

# Asynchronous usage
async def verify_business():
    response = await api.start_kyb_agent_job_async(kyb_input)
    job = await api.get_job_by_id_async(
        response['job_id'],
        include_check_results=True
    )
    return job
```

## 🔍 Detailed Usage

### KYC Verification

```python
from parcha_api import KYCAgentJobInput

kyc_input = KYCAgentJobInput(
    agent_key="your_agent_key",
    kyc_schema={
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
        "nationality": "US"
    }
)

response = api.start_kyc_agent_job(kyc_input)
```

### Running Specific Checks

```python
from parcha_api import CheckJobInput

check = CheckJobInput(
    check_id="specific_check_id",
    agent_key="your_agent_key",
    kyb_schema={
        "business_name": "Acme Corp"
    }
)

result = api.run_check(check)
```

### Retrieving Job Results

```python
# Get a single job with full details
job = api.get_job_by_id(
    job_id="job_id_here",
    include_check_results=True,
    include_status_messages=True
)

# Get all jobs for a case
jobs = api.get_jobs_by_case_id(
    case_id="case_id_here",
    agent_key="your_agent_key"
)
```

## 📋 Requirements

- Python 3.8+
- `requests` ^2.32.3
- `aiohttp` ^3.10.5
- `pydantic` ^2.9.0

## 🔒 Authentication

To use the Parcha API, you'll need:
1. An API token from your [Parcha dashboard](https://app.parcha.ai)
2. Agent keys for the specific verification services you want to use

## 📚 Documentation

For detailed API documentation, visit [docs.parcha.ai](https://docs.parcha.ai).

## 🤝 Support

- Email: support@parcha.ai
- Documentation: [docs.parcha.ai](https://docs.parcha.ai)
- Issue Tracker: [GitHub Issues](https://github.com/parcha-ai/parcha-api-python/issues)

## 📜 License

This Parcha API Client is proprietary software belonging to Parcha Labs Inc. 
All rights reserved. Use of this software is subject to the terms of your service agreement with Parcha Labs Inc.

For questions about licensing or usage, please contact support@parcha.ai.
