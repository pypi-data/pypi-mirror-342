from typing import Dict, List, Optional
from pydantic import BaseModel


class KYBSchema(BaseModel):
    """
    Schema for KYB (Know Your Business) data.
    """

    business_name: str
    # Add other fields as needed


class KYCSchema(BaseModel):
    """
    Schema for KYC (Know Your Customer) data.
    """

    first_name: str
    last_name: str
    # Add other fields as needed


class RunConfig(BaseModel):
    """
    Configuration for running a job.
    """

    # Add fields as needed
    pass


class EvalConfig(BaseModel):
    """
    Configuration for evaluating a job.
    """

    eval_name: Optional[str] = None
    scorers: Optional[List[str]] = None
    project_name: Optional[str] = None
    expected_results: Optional[Dict] = None


class KYBAgentJobInput(BaseModel):
    """
    Input data for starting a KYB agent job.
    """

    agent_key: str
    kyb_schema: Dict  # TODO: bring the actual schema from our codebase.
    webhook_url: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    run_config: Optional[RunConfig] = None
    check_ids: Optional[List[str]] = None
    run_in_parallel: Optional[bool] = False
    eval_config: Optional[EvalConfig] = None
    batch_id: Optional[str] = None


class KYCAgentJobInput(BaseModel):
    """
    Input data for starting a KYC agent job.
    """

    agent_key: str
    kyc_schema: Dict  # TODO: bring the actual schema from our codebase.
    webhook_url: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    run_config: Optional[RunConfig] = None
    check_ids: Optional[List[str]] = None
    run_in_parallel: Optional[bool] = True
    eval_config: Optional[EvalConfig] = None
    batch_id: Optional[str] = None


class CheckJobInput(BaseModel):
    """
    Input data for running a check job.
    """

    check_id: str
    agent_key: str
    kyb_schema: Optional[Dict] = None
    kyc_schema: Optional[Dict] = None


class JobResponse(BaseModel):
    """
    Response data for a job.
    """

    job_id: str
    status: str
    # Add other fields as needed
