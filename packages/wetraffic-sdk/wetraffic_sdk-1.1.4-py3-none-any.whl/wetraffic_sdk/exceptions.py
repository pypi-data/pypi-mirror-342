# exceptions.py
from typing import Any, Optional

from requests import Response


class WetrafficError(Exception):
    """Base exception for all Wetraffic errors"""

    pass


class MissingApiKeyError(Exception):
    """API key is missing"""

    pass


class AuthenticationError(WetrafficError):
    """Authentication and session related errors"""

    pass


class SessionError(AuthenticationError):
    """Session token errors"""

    def __init__(self, message: str, response_data: Optional[Any] = None):
        super().__init__(message)
        self.response_data = response_data


class UnauthorizedError(AuthenticationError):
    """Unauthorized access errors"""

    pass


class ApiError(WetrafficError):
    """API communication errors"""

    def __init__(self, message: str, response: Optional[Response] = None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response else None


class InvalidResponseError(ApiError):
    """API returned invalid/unexpected data"""

    pass


class RpcError(ApiError):
    """RPC specific errors"""

    def __init__(self, action: str, message: str, response: Optional[Response] = None):
        super().__init__(f"{message} (action: {action})", response)
        self.action = action


class TooManyDaysError(ApiError):
    """Too many days requested"""

    pass
