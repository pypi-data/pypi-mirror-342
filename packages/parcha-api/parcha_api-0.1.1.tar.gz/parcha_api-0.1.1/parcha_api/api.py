import aiohttp
import requests
from typing import Dict, List, Optional
from .models import KYBAgentJobInput, KYCAgentJobInput, CheckJobInput, JobResponse


class ParchaAPI:
    """
    A client for interacting with the Parcha API.

    This class provides methods for making both synchronous and asynchronous
    requests to various endpoints of the Parcha API.
    """

    def __init__(self, base_url: str, token: str):
        """
        Initialize the ParchaAPI client.

        Args:
            base_url (str): The base URL of the Parcha API.
            token (str): The authentication token for API requests.
        """
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None):
        """
        Make a synchronous HTTP request to the Parcha API.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The API endpoint to call.
            data (Optional[Dict]): The request body data.
            params (Optional[Dict]): The query parameters for the request.

        Returns:
            The JSON response from the API.

        Raises:
            requests.HTTPError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        response.raise_for_status()
        return response.json()

    async def _make_async_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None
    ):
        """
        Make an asynchronous HTTP request to the Parcha API.

        Args:
            method (str): The HTTP method for the request.
            endpoint (str): The API endpoint to call.
            data (Optional[Dict]): The request body data.
            params (Optional[Dict]): The query parameters for the request.

        Returns:
            The JSON response from the API.

        Raises:
            aiohttp.ClientResponseError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        headers = self.headers
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method, url, headers=headers, json=data, params=params) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientResponseError as e:
            # logger.error("request_failed", url=url, method=method, status=e.status, message=e.message, exc_info=e)
            raise

    def start_kyb_agent_job(self, agent_input: KYBAgentJobInput):
        """
        Start a KYB agent job.

        Args:
            agent_input (KYBAgentJobInput): The input data for the KYB agent job.

        Returns:
            The response from the API for starting a KYB agent job.
        """
        return self._make_request("POST", "/startKYBAgentJob", data=agent_input.model_dump())

    async def start_kyb_agent_job_async(self, agent_input: KYBAgentJobInput):
        """
        Start a KYB agent job asynchronously.

        Args:
            agent_input (KYBAgentJobInput): The input data for the KYB agent job.

        Returns:
            The response from the API for starting a KYB agent job.
        """
        return await self._make_async_request("POST", "/startKYBAgentJob", data=agent_input.model_dump())

    def start_kyc_agent_job(self, agent_input: KYCAgentJobInput):
        """
        Start a KYC agent job.

        Args:
            agent_input (KYCAgentJobInput): The input data for the KYC agent job.

        Returns:
            The response from the API for starting a KYC agent job.
        """
        return self._make_request("POST", "/startKYCAgentJob", data=agent_input.model_dump())

    async def start_kyc_agent_job_async(self, agent_input: KYCAgentJobInput):
        """
        Start a KYC agent job asynchronously.

        Args:
            agent_input (KYCAgentJobInput): The input data for the KYC agent job.

        Returns:
            The response from the API for starting a KYC agent job.
        """
        return await self._make_async_request("POST", "/startKYCAgentJob", data=agent_input.model_dump())

    def run_check(self, check_job_input: CheckJobInput) -> Dict:  # TODO use pydantic.
        """
        Run a check job.

        Args:
            check_job_input (CheckJobInput): The input data for the check job.

        Returns:
            JobResponse: The response from the API for running a check job.
        """
        return self._make_request("POST", "/runCheck", data=check_job_input.model_dump())

    async def run_check_async(self, check_job_input: CheckJobInput):
        """
        Run a check job asynchronously.

        Args:
            check_job_input (CheckJobInput): The input data for the check job.

        Returns:
            The response from the API for running a check job.
        """
        return await self._make_async_request("POST", "/runCheck", data=check_job_input.model_dump())

    def get_job_by_id(
        self,
        job_id: str,
        include_check_result_ids: bool = False,
        include_check_results: bool = False,
        include_status_messages: bool = False,
    ) -> Dict:  # TODO use pydantic.
        """
        Get a job by its ID.

        Args:
            job_id (str): The ID of the job to retrieve.
            include_check_result_ids (bool): Whether to include check result IDs in the response.
            include_check_results (bool): Whether to include check results in the response.
            include_status_messages (bool): Whether to include status messages in the response.

        Returns:
            JobResponse: The job information.
        """
        params = {
            "job_id": job_id,
            "include_check_result_ids": include_check_result_ids,
            "include_check_results": include_check_results,
            "include_status_messages": include_status_messages,
        }
        return self._make_request("GET", "/getJobById", params=params)

    async def get_job_by_id_async(
        self,
        job_id: str,
        include_check_result_ids: bool = False,
        include_check_results: bool = False,
        include_status_messages: bool = False,
    ) -> Dict:  # TODO use pydantic.
        """
        Get a job by its ID asynchronously.

        Args:
            job_id (str): The ID of the job to retrieve.
            include_check_result_ids (bool): Whether to include check result IDs in the response.
            include_check_results (bool): Whether to include check results in the response.
            include_status_messages (bool): Whether to include status messages in the response.

        Returns:
            JobResponse: The job information.
        """
        params = {
            "job_id": job_id,
            "include_check_result_ids": include_check_result_ids,
            "include_check_results": include_check_results,
            "include_status_messages": include_status_messages,
        }
        return await self._make_async_request("GET", "/getJobById", params=params)

    def get_jobs_by_case_id(
        self, case_id: str, agent_key: str, include_check_results: bool = False, include_status_messages: bool = False
    ) -> List[Dict]:  # TODO use pydantic.
        """
        Get jobs by case ID.

        Args:
            case_id (str): The ID of the case to retrieve jobs for.
            agent_key (str): The key of the agent.
            include_check_results (bool): Whether to include check results in the response.
            include_status_messages (bool): Whether to include status messages in the response.

        Returns:
            List[JobResponse]: A list of jobs for the given case ID.
        """
        params = {
            "case_id": case_id,
            "agent_key": agent_key,
            "include_check_results": include_check_results,
            "include_status_messages": include_status_messages,
        }
        return self._make_request("GET", "/getJobsByCaseId", params=params)

    async def get_jobs_by_case_id_async(
        self, case_id: str, agent_key: str, include_check_results: bool = False, include_status_messages: bool = False
    ) -> List[Dict]:  # TODO use pydantic.
        """
        Get jobs by case ID asynchronously.

        Args:
            case_id (str): The ID of the case to retrieve jobs for.
            agent_key (str): The key of the agent.
            include_check_results (bool): Whether to include check results in the response.
            include_status_messages (bool): Whether to include status messages in the response.

        Returns:
            List[JobResponse]: A list of jobs for the given case ID.
        """
        params = {
            "case_id": case_id,
            "agent_key": agent_key,
            "include_check_results": include_check_results,
            "include_status_messages": include_status_messages,
        }
        return await self._make_async_request("GET", "/getJobsByCaseId", params=params)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Get API token from environment variable
    api_token = os.getenv("PARCHA_API_TOKEN")
    if not api_token:
        raise ValueError("PARCHA_API_TOKEN not found in environment variables")

    # Initialize the API client
    api = ParchaAPI(os.getenv("PARCHA_BASE_URL"), api_token)

    # Test various API methods
    try:
        # Get jobs by case ID
        jobs = api.get_jobs_by_case_id("macron", "parcha-v0")
        print("Jobs for case:", jobs)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
