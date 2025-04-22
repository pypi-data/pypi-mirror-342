"""Exception classes for the VisionFi client."""

from typing import Optional


class VisionFiError(Exception):
    """Base exception for all VisionFi client errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        """Initialize a VisionFiError.

        Args:
            message: Human-readable error description
            status_code: HTTP status code (if applicable)
            code: Error code string (if available)
            details: Additional error details (if available)
        """
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return a string representation of the error."""
        parts = [self.message]
        if self.code:
            parts.append(f"Code: {self.code}")
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        return " | ".join(parts)


class AuthenticationError(VisionFiError):
    """Error related to authentication failures."""

    pass


class ApiError(VisionFiError):
    """Error returned by the VisionFi API."""

    pass


class ConnectionError(VisionFiError):
    """Error related to network or connection issues."""

    pass