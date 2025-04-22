"""Utility functions for the VisionFi client."""

import time
from typing import Any, Callable, Dict, Optional, TypeVar

from .exceptions import VisionFiError

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exception_types: tuple = (Exception,),
) -> T:
    """Retry a function with exponential backoff.

    Args:
        func: Function to retry
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Factor by which delay increases each retry
        exception_types: Exception types to catch and retry

    Returns:
        The return value of the function

    Raises:
        The last exception raised by the function if all attempts fail
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_attempts):
        try:
            return func()
        except exception_types as e:
            last_exception = e
            if attempt == max_attempts - 1:
                raise
            time.sleep(delay)
            delay *= backoff_factor

    # This should never be reached, but just in case
    if last_exception:
        raise last_exception
    raise VisionFiError("Unknown error in retry_with_backoff")


def parse_api_error(response_data: Dict[str, Any]) -> VisionFiError:
    """Parse an API error response into a VisionFiError.

    Args:
        response_data: The error response data

    Returns:
        A VisionFiError with details from the response
    """
    message = response_data.get("message", "Unknown API error")
    code = response_data.get("code")
    details = response_data.get("details")
    
    return VisionFiError(
        message=message,
        code=code,
        details=details,
    )


def handle_file_data(file_data: Any) -> bytes:
    """Ensure file data is in the correct format.

    Args:
        file_data: File data as bytes, file-like object, or string path

    Returns:
        File data as bytes

    Raises:
        VisionFiError: If file_data is not in a supported format
    """
    if isinstance(file_data, bytes):
        return file_data
    
    # If it's a file-like object, read it
    if hasattr(file_data, "read") and callable(file_data.read):
        return file_data.read()
    
    # If it's a string, try to interpret it as a file path
    if isinstance(file_data, str):
        try:
            with open(file_data, "rb") as f:
                return f.read()
        except Exception as e:
            raise VisionFiError(f"Failed to read file at path {file_data}: {str(e)}")
    
    raise VisionFiError(
        "Invalid file_data format. Expected bytes, file-like object, or file path."
    )