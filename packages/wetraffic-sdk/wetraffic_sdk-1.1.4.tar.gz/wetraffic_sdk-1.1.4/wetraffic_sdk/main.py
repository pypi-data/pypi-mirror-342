from typing import Optional

from .api_client import ApiClient
from .flow import Flow
from .lights import Lights
from .real_time_map import RealTimeMap


class WetrafficSdk:
    """
    Main class for the Wetraffic SDK.

    This class provides the main interface for interacting with the Wetraffic services.
    Requires WETRAFFIC_API_KEY environment variable to be set before initialization.

    Args:
        area_prefix (str): The area prefix (leftmost domain) to initialize the SDK with.
        area_id (Optional[str]): The area ID to initialize the SDK with.

    Attributes:
        lights (Lights): Interface for managing traffic lights.
        flow (Flow): Interface for managing Flow devices.
        real_time_map (RealTimeMap): Interface for interacting with real-time map data

    Raises:
        MissingApiKeyError: If WETRAFFIC_API_KEY environment variable is not set.

    Example:
        >>> import os
        >>> os.environ["WETRAFFIC_API_KEY"] = "your-api-key"
        >>> from wetraffic_sdk import WetrafficSdk
        >>> wt = WetrafficSdk(area="area01")
    """

    def __init__(self, area_prefix: str, use_staging: Optional[bool] = None, area_id: Optional[str] = None):
        self._client = ApiClient(area_prefix=area_prefix, use_staging=use_staging, area_id=area_id)
        self.lights = Lights(client=self._client)
        self.flow = Flow(client=self._client)
        self.real_time_map = RealTimeMap(client=self._client)
