"""Authentication utilities for the VisionFi client."""

import json
import os.path
from typing import Dict, Optional, Union

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError

from .exceptions import AuthenticationError


class ServiceAccountAuth:
    """Service account authentication for VisionFi API."""

    def __init__(
        self,
        service_account_path: Optional[str] = None,
        service_account_json: Optional[Dict] = None,
    ):
        """Initialize service account authentication.

        Args:
            service_account_path: Path to service account JSON file
            service_account_json: Service account credentials as a dictionary

        Raises:
            AuthenticationError: If no valid service account credentials are provided
        """
        if not service_account_path and not service_account_json:
            raise AuthenticationError(
                "Either service_account_path or service_account_json must be provided"
            )
        
        try:
            if service_account_path:
                if not os.path.isfile(service_account_path):
                    raise AuthenticationError(
                        f"Service account file not found: {service_account_path}"
                    )
                # Store both the path and the parsed JSON for different token methods
                self.service_account_path = service_account_path
                with open(service_account_path, 'r') as f:
                    self.service_account_json = json.load(f)
                
                # Create standard credentials with scopes
                self.credentials = service_account.Credentials.from_service_account_file(
                    service_account_path,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
            else:
                # Store the provided JSON
                self.service_account_json = service_account_json
                self.service_account_path = None
                
                # Create standard credentials with scopes
                self.credentials = service_account.Credentials.from_service_account_info(
                    service_account_json,
                    scopes=["https://www.googleapis.com/auth/cloud-platform"]
                )
            
            # Store the request object for token refresh
            self.request = Request()
            
        except Exception as e:
            raise AuthenticationError(f"Failed to initialize service account: {str(e)}")

    def get_id_token(self, audience: str = "platform.visionfi.ai") -> str:
        """Get a JWT ID token for the specified audience.
        
        Args:
            audience: The audience claim for the JWT ID token (default is "platform.visionfi.ai")

        Returns:
            str: The JWT ID token

        Raises:
            AuthenticationError: If JWT token generation fails
        """
        try:
            # For service account authentication with ID tokens, we'll need to use 
            # IDTokenCredentials from google.oauth2.service_account
            from google.oauth2 import service_account
            
            # Create credentials specific for ID tokens with the desired audience
            if self.service_account_path:
                id_credentials = service_account.IDTokenCredentials.from_service_account_file(
                    self.service_account_path,
                    target_audience=audience
                )
            else:
                id_credentials = service_account.IDTokenCredentials.from_service_account_info(
                    self.service_account_json,
                    target_audience=audience
                )
            
            # Refresh to get a new token
            id_credentials.refresh(self.request)
            
            # Return the ID token
            return id_credentials.token
            
        except GoogleAuthError as e:
            raise AuthenticationError(f"Failed to generate ID token: {str(e)}")
        except Exception as e:
            raise AuthenticationError(f"Unexpected error generating ID token: {str(e)}")

    def get_authorization_header(self, audience: str = "platform.visionfi.ai") -> Dict[str, str]:
        """Get authorization header with JWT bearer token.

        Args:
            audience: The audience for the JWT token (default is "platform.visionfi.ai")

        Returns:
            Dict[str, str]: The authorization header with JWT
        """
        return {"Authorization": f"Bearer {self.get_id_token(audience)}"}