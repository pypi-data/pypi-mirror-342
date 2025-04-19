import json
from datetime import datetime as dt
from datetime import time, timezone
from typing import Optional

from pydantic import BaseModel, Field

from .api_client import ApiClient
from .logging_config import setup_logger
from .utils import get_start_date

logger = setup_logger()


def get_human_readable_lights_status(status: list[int] | None) -> None | str:
    """
    Get the human readable status of the traffic lights.

    Args:
        status (list[int]): status

    Returns:
        str: human readable status
    """
    if status is None:
        return None
    t = ""

    if len(status) >= 1:
        if status[0] == 0:
            t = "Normal mode"
        elif status[0] == 1:
            t = "Flashing yellow yields"
        elif status[0] == 2 or status[0] == 3:
            t = "Flashing yellow"
        elif status[0] == 4:
            t = "Dark"
        elif status[0] == 5:
            t = "Manual stage"
        elif status[0] == 10 or status[0] == 11:
            t = "Failure - Dark"
        elif status[0] == 12 or status[0] == 13:
            t = "Failure - Flashing yellow"
        elif status[0] == 14:
            if len(status) >= 2:
                status_1 = status[1]
                if status_1 == 1:
                    t = "HW.BIN"
                elif status_1 == 2:
                    t = "SW.BIN"
                elif status_1 == 3:
                    t = "PR.BIN"
                elif status_1 == 4:
                    t = "VR.BIN"
                elif status_1 == 5:
                    t = "GSM.BIN"
                elif status_1 == 6:
                    t = "PTC.BIN"
                elif status_1 == 7:
                    t = "TA library"
                elif status_1 == 20:
                    t = "identification"
                elif status_1 == 21:
                    t = "SWC"
                elif status_1 == 22:
                    t = "BUS"
                elif status_1 == 190:
                    t = "SD card"
                elif status_1 == 191:
                    t = "ext.storage"
                elif status_1 == 192:
                    t = "timing"
                elif status_1 == 193:
                    t = "memory"
                elif status_1 == 200:
                    t = "spindriver"
                elif status_1 == 201:
                    t = "feigdriver"
                elif status_1 == 202:
                    t = "gpsdriver"
                elif status_1 == 203:
                    t = "ifacedriver"
                elif status_1 == 205:
                    t = "ocitdriver"
                else:
                    if status[1] >= 101 and status[1] < 128:
                        t = "registration"
                if t:
                    t = " (" + t + ")"
                t = "Control Unit error" + t
        elif status[0] == 15:
            t = "Failure - Bus reset"
        elif status[0] == 16:
            t = "Power failure"

        if status[0] < 10 and status[0] != 3 and len(status) > 1:
            tp = ""
            status_bits = status[1] & 7
            if status_bits == 0:
                tp = "local schedule"
            elif status_bits == 1:
                tp = "local control"
            elif status_bits == 2:
                tp = "service PC"
            elif status_bits == 3:
                tp = "OEM control"
            elif status_bits == 4:
                tp = "central"

            if status[1] & 8:
                if tp:
                    tp += ", "
                tp += "coordination"
            if status[1] & 16:
                if tp:
                    tp += ", "
                tp += "TA"
            if tp:
                t += " (" + tp + ")"
    return t or None


class LightConfig(BaseModel):
    id: str = Field(description="Unique identifier of the traffic light")
    name: str = Field(description="Display name of the traffic light")
    lat: float = Field(description="Latitude coordinate of the traffic light location")
    lon: float = Field(description="Longitude coordinate of the traffic light location")
    installed_at: dt = Field(description="Installation date and time of the traffic light")


class LightsStatus(BaseModel):
    datetime: dt = Field(description="Timestamp of the status reading")
    human_readable_status: Optional[str] = Field(
        default=None, description="Human readable interpretation of the traffic light status"
    )
    raw_status: Optional[list[int]] = Field(
        default=None,
        description="Raw status values from the traffic light controller",
        examples=[
            [0, 1, 0],
        ],
    )
    plan: Optional[str] = Field(default=None, description="Active traffic plan identifier at the time of reading")
    router_is_connected: bool = Field(description="Whether the traffic light controller is connected to the network")


class Lights:
    """
    Interface for managing traffic lights.

    This class provides methods to interact with traffic lights data and status.
    """

    def __init__(self, *, client: ApiClient):
        self.client = client
        self.area_id = self.client.area_id

    def get_devices(self) -> list[LightConfig]:
        """
        Get the configuration of all traffic lights in the area.

        Returns:
            list[LightConfig]: List of traffic light configurations containing ID, location and settings

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> wt.lights.get_devices()
        """
        response = self.client.invoke_rpc(
            action="get_lights_config",
            params={
                "area": self.area_id,
            },
        )
        return [LightConfig(**light) for light in response["lights"]]

    def get_load_dates(self, *, year: int, device_id: str) -> list[dt]:
        """
        Get the dates when traffic load data is available for a specific traffic light.

        Args:
            year (int): Year to query the load data for
            device_id (str): Identifier of the traffic light

        Returns:
            list[datetime]: List of UTC dates when load data is available

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.lights.get_load_dates(year=2023, device_id="test-id")
            >>> # Returns a list of datetime objects:
            >>> # [datetime(2023, 1, 1, 0, 0), datetime(2023, 1, 2, 0, 0)]
        """
        response = self.client.invoke_rpc(
            action="get_lights_loads",
            params={
                "area": self.area_id,
                "id": device_id,
                "month": str(year),
            },
        )
        return [dt.fromisoformat(date_str).replace(tzinfo=timezone.utc) for date_str in response]

    def get_historical_status_data(self, *, device_id: str, end_date: dt, days: int = 1) -> list[LightsStatus]:
        """
        Get the historical status data for a specific traffic light.

        Args:
            device_id (str): Identifier of the traffic light
            end_date (datetime): End date for the data retrieval period
            days (int, optional): Number of days to look back from end_date. Must be between 1 and 15.

        Returns:
            list[LightsStatus]: List of status records containing connection state, plan and light status information

        Raises:
            TooManyDaysError: If days is exceeds max number allowed

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> status = wt.lights.get_historical_status_data(
            ...     device_id="test-id",
            ...     end_date=datetime(2023, 1, 1, 0, 0),
            ...     days=10
            ... )
        """
        min_datetime = get_start_date(end_date=end_date, days=days)
        end_datetime = dt.combine(end_date, time.max)
        logger.debug("Requesting historical status data...", extra={"device_id": device_id, "days": days})
        response = self.client.invoke_rpc(
            action="get_lights_status_data",
            params={
                "area": self.area_id,
                "id": device_id,
                "min_datetime": min_datetime.isoformat(),
                "max_datetime": end_datetime.isoformat(),
            },
        )

        datetime_index = 0  # date iso format
        code_status_index = 8  # "200" = connection OK
        plan_index = 13  # Plan info status
        status_index = 18  # "[int, int,int]" string"
        router_status_index = 19  # boolean or null
        result_list: list[LightsStatus] = []

        for data in response:
            datetime_str = data[datetime_index]
            assert isinstance(datetime_str, str), "datetime_str is not a string"
            datetime_obj = dt.fromisoformat(datetime_str)
            code_status = data[code_status_index]
            light_is_connected = code_status == "200"
            status = data[status_index]
            status_list = json.loads(status) if status is not None else None
            router_status = data[router_status_index]
            plan = data[plan_index]
            result_list.append(
                LightsStatus(
                    datetime=datetime_obj,
                    human_readable_status=get_human_readable_lights_status(status_list),
                    raw_status=status_list,
                    plan=plan,
                    router_is_connected=router_status is True or light_is_connected,
                )
            )
        return result_list
