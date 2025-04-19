import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Literal, Optional
from urllib.parse import urljoin

from pydantic import BaseModel, validate_call
from requests import HTTPError, get

from .constants import (
    API_ENDPOINT,
    API_ENDPOINT_STAGING,
    FEATURES_BUCKET_DISTRIBUTION_URL,
    FLOW_DATA_MANAGEMENT_API_ENDPOINT,
    PG_API_URL,
)
from .exceptions import (
    InvalidResponseError,
    MissingApiKeyError,
    RpcError,
    SessionError,
    UnauthorizedError,
    WetrafficError,
)
from .logging_config import setup_logger


class RpcRequest(BaseModel):
    action: str
    params: dict[str, Any]


logger = setup_logger()


class ApiClient:
    SESSION_EXPIRATION_BUFFER = timedelta(minutes=5)

    @validate_call
    def __init__(self, *, area_prefix: str, area_id: Optional[str] = None, use_staging: Optional[bool] = None):
        api_key = os.environ.get("WETRAFFIC_API_KEY")
        if not api_key:
            log_extra = {"area_prefix": area_prefix, "reason": "WETRAFFIC_API_KEY not set"}
            logger.critical("SDK Initialization failed", extra=log_extra)
            raise MissingApiKeyError("WETRAFFIC_API_KEY not set.")

        self.api_key: str = api_key
        self.area_prefix = area_prefix
        self.area_id = area_id or area_prefix
        self.session_token: Optional[str] = None
        self.session_expiration_date = datetime.min
        self.use_staging = use_staging or os.environ.get("WETRAFFIC_USE_STAGING") == "true"
        self.endpoint = API_ENDPOINT if self.use_staging is not True else API_ENDPOINT_STAGING

    def _send_rpc_request(self, *, request: RpcRequest, headers: Optional[dict] = {}) -> Any:
        try:
            response = get(
                self.endpoint,
                headers=headers,
                params={"message": json.dumps(request.model_dump(), separators=(",", ":"))},
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            if http_err.response.status_code in [410, 403]:
                raise UnauthorizedError("Unauthorized access", http_err.response)
            raise RpcError(request.action, "RPC call failed", http_err.response) from http_err
        except Exception as e:
            raise WetrafficError(f"Unexpected error during RPC: {str(e)}") from e

    def _is_session_valid(self) -> bool:
        if self.session_token is None:
            return False
        now_utc = datetime.now(timezone.utc)
        is_valid = self.session_expiration_date > (now_utc + self.SESSION_EXPIRATION_BUFFER)
        return is_valid

    def _upsert_session_token(self):
        data = self._send_rpc_request(
            request=RpcRequest(
                action="get_session_token",
                params={
                    "area": self.area_prefix,
                    "api_key": self.api_key,
                },
            )
        )
        new_token = data.get("token")
        new_iso_date = data.get("token_expiration")
        if not new_token or not new_iso_date:
            raise InvalidResponseError("Incomplete session data", data)
        self.session_token = new_token
        self.session_expiration_date = datetime.fromisoformat(new_iso_date)

    def _manage_session(self):
        if not self._is_session_valid():
            self._upsert_session_token()
        if not self.session_token:
            raise SessionError("Session token unavailable for RPC call")

    @validate_call
    def invoke_rpc(self, *, action: str, params: dict) -> Any:
        self._manage_session()
        headers = {"Authorization": f"Bearer {self.session_token}"}
        request = RpcRequest(action=action, params=params)
        return self._send_rpc_request(request=request, headers=headers)

    @validate_call
    def send_pg_api_request(
        self,
        *,
        path: str,
        params: dict,
    ) -> Any:
        self._manage_session()
        headers = {"Authorization": f"Bearer {self.session_token}", "Content-Type": "application/json"}
        request = get(urljoin(PG_API_URL, path), headers=headers, params=params)
        request.raise_for_status()
        return request.json()

    @validate_call
    def send_flow_data_management_api_request(self, *, path: Literal["data", "loads"] = "data", params: dict) -> Any:
        url = FLOW_DATA_MANAGEMENT_API_ENDPOINT + path
        request = get(url, params=params)
        request.raise_for_status()
        return request.json()

    @validate_call
    def get_asset_from_features_bucket(self, path: str):
        request = get(urljoin(FEATURES_BUCKET_DISTRIBUTION_URL, path))
        request.raise_for_status()
        return request.json()
