"""VisionFi client implementation."""

import json
import time
from datetime import datetime
from typing import Any, Dict, Optional, Union

import requests
from requests.exceptions import RequestException

from .auth import ServiceAccountAuth
from .exceptions import ApiError, AuthenticationError, ConnectionError, VisionFiError
from .visionfi_types import (
    AnalysisJob,
    AnalysisResult,
    AnalyzeDocumentOptions,
    AuthTokenResult,
    AuthVerificationResult,
    ClientInfoResponse,
    WorkflowsResponse,
)
from .utils import handle_file_data, parse_api_error


class VisionFi:
    """VisionFi API client."""

    def __init__(
        self,
        service_account_path: Optional[str] = None,
        service_account_json: Optional[Dict] = None,
        api_endpoint: str = "https://platform.visionfi.ai/api/v1",
        timeout: int = 60,
    ):
        """Initialize the VisionFi client.

        Args:
            service_account_path: Path to service account JSON file
            service_account_json: Service account credentials as a dictionary
            api_endpoint: VisionFi API endpoint
            timeout: Default request timeout in seconds

        Raises:
            AuthenticationError: If no valid service account credentials are provided
        """
        self.api_endpoint = api_endpoint.rstrip("/")
        self.timeout = timeout
        
        # Initialize auth
        self.auth = ServiceAccountAuth(
            service_account_path=service_account_path,
            service_account_json=service_account_json,
        )
        
        # Initialize session
        self.session = requests.Session()

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ) -> Dict:
        """Make an authenticated request to the VisionFi API.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (without leading slash)
            params: Query parameters
            data: Form data
            json_data: JSON data
            files: Files to upload
            timeout: Request timeout in seconds (defaults to self.timeout)

        Returns:
            Dict: API response

        Raises:
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
            VisionFiError: If an unexpected error occurs
        """
        url = f"{self.api_endpoint}/{path}"
        timeout = timeout or self.timeout
        
        try:
            # Get fresh auth headers for each request
            headers = self.auth.get_authorization_header("platform.visionfi.ai")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                files=files,
                headers=headers,
                timeout=timeout,
            )
            
            # Try to parse response as JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"message": response.text}
            
            # Handle error responses
            if not response.ok:
                error = parse_api_error(response_data)
                error.status_code = response.status_code
                raise ApiError(
                    message=error.message,
                    status_code=error.status_code,
                    code=error.code,
                    details=error.details,
                )
            
            return response_data
        
        except RequestException as e:
            raise ConnectionError(f"Network error: {str(e)}")
        except ApiError:
            raise  # Re-raise API errors
        except Exception as e:
            raise VisionFiError(f"Unexpected error: {str(e)}")

    def verify_auth(self) -> AuthVerificationResult:
        """Verify authentication with the VisionFi API.

        Returns:
            AuthVerificationResult: Authentication verification result

        Raises:
            AuthenticationError: If authentication fails
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
        """
        try:
            response = self._make_request("POST", "auth/verify")
            
            # Handle potential different response formats
            if isinstance(response, bool):
                # If API just returns a boolean
                return AuthVerificationResult(success=True, data={"authenticated": response})
            elif isinstance(response, dict) and "data" in response:
                # Standard format
                return AuthVerificationResult(**response)
            elif isinstance(response, dict):
                # If API returns a dict but without the expected wrapper
                return AuthVerificationResult(success=True, data=response)
            else:
                # Fallback for any other format
                return AuthVerificationResult(success=True, data={"response": response})
                
        except ApiError as e:
            if e.status_code == 401:
                raise AuthenticationError(
                    f"Authentication failed: {e.message}", 
                    status_code=e.status_code, 
                    code=e.code
                )
            raise

    def get_auth_token(self) -> AuthTokenResult:
        """Get an authentication token for external use.

        Returns:
            AuthTokenResult: Authentication token result

        Raises:
            AuthenticationError: If token retrieval fails
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
        """
        try:
            response = self._make_request("POST", "auth/token")
            
            # Handle potential different response formats
            if isinstance(response, dict) and "data" in response:
                # Standard format
                return AuthTokenResult(**response)
            elif isinstance(response, dict):
                # If API returns a dict but without the expected wrapper
                return AuthTokenResult(success=True, data=response)
            elif isinstance(response, str):
                # If API just returns a token string
                return AuthTokenResult(success=True, data={"token": response})
            else:
                # Fallback for any other format
                return AuthTokenResult(success=True, data={"response": str(response)})
        except ApiError as e:
            if e.status_code == 401:
                raise AuthenticationError(
                    f"Token retrieval failed: {e.message}", 
                    status_code=e.status_code, 
                    code=e.code
                )
            raise

    def get_client_info(self) -> ClientInfoResponse:
        """Get client account information.

        Returns:
            ClientInfoResponse: Client information

        Raises:
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
        """
        response = self._make_request("GET", "operations/getClientInfo")
        
        # Handle potential different response formats
        if isinstance(response, dict) and "data" in response:
            # Standard format
            return ClientInfoResponse(**response)
        elif isinstance(response, dict):
            # If API returns a dict but without the expected wrapper
            return ClientInfoResponse(success=True, data=response)
        else:
            # Fallback for any other format
            return ClientInfoResponse(success=True, data={"response": response})

    def get_workflows(self) -> WorkflowsResponse:
        """Get available document analysis workflows.

        Returns:
            WorkflowsResponse: Available workflows

        Raises:
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
        """
        response = self._make_request("GET", "operations/getAvailableWorkflows")
        
        # Handle potential different response formats
        if isinstance(response, dict) and "data" in response:
            # Standard format
            return WorkflowsResponse(**response)
        elif isinstance(response, dict):
            # If API returns a dict but without the expected wrapper
            return WorkflowsResponse(success=True, data=response)
        elif isinstance(response, list):
            # If API returns a list of workflows directly
            return WorkflowsResponse(success=True, data=response)
        else:
            # Fallback for any other format
            return WorkflowsResponse(success=True, data=[])

    def analyze_document(
        self, 
        file_data: Union[bytes, str, Any], 
        options: Union[Dict, AnalyzeDocumentOptions]
    ) -> AnalysisJob:
        """Submit a document for analysis.

        Args:
            file_data: Document file data (bytes, file path, or file-like object)
            options: Analysis options (dict or AnalyzeDocumentOptions)

        Returns:
            AnalysisJob: Created analysis job

        Raises:
            VisionFiError: If file_data is invalid or options are incomplete
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
        """
        # Ensure options is a dict
        if isinstance(options, AnalyzeDocumentOptions):
            options_dict = options.dict()
        else:
            options_dict = dict(options)
        
        # Ensure required options are present
        if "file_name" not in options_dict:
            raise VisionFiError("file_name is required in options")
        if "analysis_type" not in options_dict:
            raise VisionFiError("analysis_type is required in options")
        
        # Prepare file data
        file_bytes = handle_file_data(file_data)
        
        # Convert to base64 to match TypeScript client
        import base64
        file_base64 = base64.b64encode(file_bytes).decode('utf-8')
        
        # Prepare request data
        request_data = {
            "fileName": options_dict["file_name"],
            "fileBase64": file_base64,
            "analysisType": options_dict["analysis_type"]
        }
        
        # Add any additional options
        if "workflow_key" in options_dict:
            request_data["workflowKey"] = options_dict["workflow_key"]
        if "metadata" in options_dict:
            request_data["metadata"] = options_dict["metadata"]
            
        # Submit analysis request
        response = self._make_request(
            method="POST", 
            path="operations/analyze", 
            json_data=request_data
        )
        
        # Handle potential different response formats
        try:
            if isinstance(response, dict) and "data" in response:
                # Standard format
                return AnalysisJob(**response["data"])
            elif isinstance(response, dict):
                # If API returns a uuid but is missing other required fields
                if "uuid" in response:
                    # Fill in missing required fields with reasonable defaults
                    job_data = {
                        "uuid": response["uuid"],
                        "status": "submitted",  # Assume job was submitted successfully
                        "created_at": datetime.now(),  # Use current time
                        "client_id": "unknown"  # Use placeholder
                    }
                    return AnalysisJob(**job_data)
                
                # Try to use response as is (might fail)
                return AnalysisJob(**response)
            else:
                # Fallback for unexpected formats
                raise VisionFiError(f"Unexpected response format from API: {response}")
        except Exception as e:
            # If all else fails, create a minimal valid object with the data we have
            if isinstance(response, dict) and "uuid" in response:
                # At least we have a UUID to return
                return AnalysisJob(
                    uuid=response["uuid"],
                    status="submitted",
                    created_at=datetime.now(),
                    client_id="unknown"
                )
            # Re-raise the error if we can't create a valid response
            raise VisionFiError(f"Failed to parse API response: {str(e)}")

    def get_results(
        self, 
        job_uuid: str, 
        poll_interval: Optional[int] = None, 
        max_attempts: Optional[int] = None,
        early_warning_attempts: Optional[int] = None,
    ) -> AnalysisResult:
        """Get analysis results, optionally with polling.

        Args:
            job_uuid: Analysis job UUID
            poll_interval: Polling interval in milliseconds (None for no polling)
            max_attempts: Maximum polling attempts (None for unlimited)
            early_warning_attempts: Number of attempts before warning (None for no warning)

        Returns:
            AnalysisResult: Analysis results

        Raises:
            ConnectionError: If a network error occurs
            ApiError: If the API returns an error
            VisionFiError: If polling times out
        """
        # Convert milliseconds to seconds for Python
        poll_seconds = (poll_interval / 1000) if poll_interval is not None else None
        
        def process_response(response, current_uuid):
            # Handle the specific response format from the API
            if isinstance(response, dict):
                # Check for the expected format with 'found' field
                if 'found' in response:
                    if response['found'] is True and response.get('results'):
                        # Results found - extract from the nested 'results' field
                        results_data = response['results']
                        
                        # Create a valid AnalysisResult object
                        return AnalysisResult(
                            uuid=results_data.get('uuid', current_uuid),
                            status=results_data.get('status', 'completed'),
                            created_at=results_data.get('processedAt', datetime.now()),
                            completed_at=results_data.get('processedAt', None),
                            results=results_data
                        )
                    else:
                        # No results found or still processing
                        return AnalysisResult(
                            uuid=current_uuid,
                            status='processing' if response.get('message') == 'No analysis results found' else 'error',
                            created_at=datetime.now(),
                            results=None,
                            error={"message": response.get('message', 'No results available')}
                        )
                
                # Try other formats as fallbacks
                if "data" in response:
                    try:
                        return AnalysisResult(**response["data"])
                    except Exception:
                        pass
                
                try:
                    return AnalysisResult(**response)
                except Exception:
                    pass
            
            # If all else fails, create a minimal valid result
            return AnalysisResult(
                uuid=current_uuid,
                status='error',
                created_at=datetime.now(),
                error={"message": "Unexpected response format", "response": str(response)}
            )
        
        # Single request if no polling
        if poll_seconds is None:
            response = self._make_request("GET", f"operations/getAnalysisResults", params={"uuid": job_uuid})
            return process_response(response, job_uuid)
        
        # Polling logic
        attempts = 0
        warned = False
        
        while True:
            response = self._make_request("GET", f"operations/getAnalysisResults", params={"uuid": job_uuid})
            result = process_response(response, job_uuid)
            
            # Return if processing is complete
            if result.status != "processing":
                return result
            
            # Check if max attempts reached
            if max_attempts is not None and attempts >= max_attempts:
                raise VisionFiError(
                    f"Polling timed out after {attempts} attempts"
                )
            
            # Check if early warning should be shown
            if (
                early_warning_attempts is not None 
                and attempts >= early_warning_attempts
                and not warned
            ):
                warned = True
                # In a real implementation, you might log a warning here
            
            # Wait before next poll
            time.sleep(poll_seconds)
            attempts += 1