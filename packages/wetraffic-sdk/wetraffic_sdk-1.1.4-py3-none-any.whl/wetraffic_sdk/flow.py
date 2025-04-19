from datetime import datetime as dt
from datetime import time, timezone
from typing import Optional

from pydantic import BaseModel, Field, validate_call

from .api_client import ApiClient
from .logging_config import setup_logger
from .utils import convert_datetime_to_iso_str, get_start_date

logger = setup_logger()


class Gate(BaseModel):
    id: str = Field(description="Unique identifier of the gate")
    name: Optional[str] = Field(default=None, description="Display name of the gate")
    coordinates: list[list[float]] = Field(
        description="List of [longitude, latitude] coordinates defining the oriented gate line"
    )


class Analytic(BaseModel):
    id: str = Field(description="Unique identifier of the analytic area")
    name: Optional[str] = Field(default=None, description="Display name of the analytic area")
    coords: Optional[tuple[float, float]] = Field(
        default=None, description="Central point coordinates as (longitude, latitude)"
    )
    gates: list[Gate] = Field(description="List of gates")


class Block(BaseModel):
    analytics: list[Analytic]


class BlockConfiguration(BaseModel):
    area: str = Field(description="Area identifier where the block is located (area_id)")
    id: str = Field(description="Unique identifier of the block configuration")
    block: Block = Field(description="Block settings and parameters")


class CameraStatus(BaseModel):
    datetime: dt = Field(description="Timestamp of the camera status check")
    status: bool = Field(description="Whether the camera is online (True) or offline (False)")


DISTRIBUTION_COLUMNS = [
    "datetime",
    "bicycle",
    "bus",
    "car",
    "scooter",
    "heavy",
    "light",
    "motorcycle",
    "pedestrian",
    "animal",
    "van",
    "other",
]

distribution_index = {key: index for index, key in enumerate(DISTRIBUTION_COLUMNS)}


class DistributionCount(BaseModel):
    datetime: dt
    bicycle: int
    bus: int
    car: int
    scooter: int
    heavy: int
    light: int
    motorcycle: int
    pedestrian: int
    animal: int
    van: int
    other: int


class Flow:
    """
    Interface for managing Flow devices.

    This class provides methods to interact with Flow devices and get traffic data and status.
    """

    def __init__(self, *, client: ApiClient):
        self.client = client
        self.area_id = self.client.area_id

    def get_devices(self) -> list[BlockConfiguration]:
        """
        Get the configuration of all Flow devices in the area.

        Returns:
            list[BlockConfiguration]: List of Flow devices configurations containing:
                - Area identifier
                - Device identifier
                - Block parameters and settings

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> wt.flow.get_devices()
        """
        data = self.client.invoke_rpc(
            action="get_blocks",
            params={},
        )
        return [BlockConfiguration(**datum) for datum in data]

    @validate_call
    def get_system_status_loads(self, *, year: int, block_id: str) -> list[dt]:
        """
        Get the dates when system status data is available for a specific Flow device.

        Args:
            year (int): Year to query the status data for
            block_id (str): Identifier of the Flow device block

        Returns:
            list[datetime]: List of UTC dates when status data is available

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.flow.get_system_status_loads(year=2023, block_id="test-id")
            >>> # Returns a list of datetime objects:
            >>> # [datetime(2023, 1, 1, 0, 0), datetime(2023, 1, 2, 0, 0)]
        """
        response = self.client.send_pg_api_request(
            path="flow_block_system_status_loads",
            params={
                "select": "load_date",
                "area_id": f"eq.{self.area_id}",
                "block_id": f"eq.{block_id}",
                "load_year": f"eq.{year}",
            },
        )
        return [dt.fromisoformat(datum["load_date"]).replace(tzinfo=timezone.utc) for datum in response]

    @validate_call
    def get_distribution_loads(self, *, year: int, analytic_id: str, gate_id: str) -> list[dt]:
        """
        Get the dates when distribution data is available for a specific gate.

        Args:
            year (int): Year to query the distribution data for
            analytic_id (str): Identifier of the analytic area
            gate_id (str): Identifier of the gate within the analytic area

        Returns:
            list[datetime]: List of UTC dates when distribution data is available

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.flow.get_distribution_loads(
            ...     year=2023,
            ...     analytic_id="test-id",
            ...     gate_id="test-id"
            ... )
        """
        response = self.client.send_flow_data_management_api_request(
            path="loads",
            params={
                "area": self.area_id,
                "analytics": analytic_id,
                "gate_id": gate_id,
                "value_type": "distribution",
                "month": str(year),  # Get more data replacing with a whole year
            },
        )
        return [dt.fromisoformat(datum) for datum in response]

    @validate_call
    def get_camera_status_loads(self, *, year: int, analytic_id: str) -> list[dt]:
        """
        Get the dates when camera status data is available.

        Args:
            year (int): Year to query the camera status for
            analytic_id (str): Identifier of the analytic area containing the camera

        Returns:
            list[datetime]: List of UTC dates when camera status data is available

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.flow.get_camera_status_loads(year=2023, analytic_id="test-id")
        """
        response = self.client.send_flow_data_management_api_request(
            path="loads",
            params={
                "area": self.area_id,
                "analytics": analytic_id,
                "value_type": "string_value",
                "month": year,  # Get more data replacing with a whole year
                "gate_id": "*",
            },
        )
        return [dt.fromisoformat(datum) for datum in response]

    @validate_call
    def get_historical_camera_status_data(self, *, analytic_id: str, end_date: dt, days: int = 1) -> list[CameraStatus]:
        """
        Get historical camera online/offline status data.

        Args:
            analytic_id (str): Identifier of the analytic area containing the camera
            end_date (datetime): End date for the data retrieval (UTC)
            days (int, optional): Number of days to look back from end_date. Defaults to 1.

        Returns:
            list[CameraStatus]: List of status records containing timestamp and online/offline state

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> status = wt.flow.get_historical_camera_status_data(
            ...     analytic_id="test-id",
            ...     end_date=datetime(2023, 1, 1),
            ...     days=1
            ... )
        """
        from_datetime = get_start_date(end_date=end_date, days=days)
        to_datetime = dt.combine(end_date, time.max)
        response = self.client.send_flow_data_management_api_request(
            path="data",
            params={
                "area": self.area_id,
                "analytics": analytic_id,
                "value_type": "string_value",
                "from_datetime": convert_datetime_to_iso_str(from_datetime),
                "to_datetime": convert_datetime_to_iso_str(to_datetime),
            },
        )
        return [CameraStatus(datetime=datum[0], status=datum[1]) for datum in response]

    @validate_call
    def get_historical_distribution_data(self, *, analytic_id: str, gate_id: str, end_date: dt, days: int = 1):
        """
        Get historical vehicle distribution data for a specific gate.

        Args:
            analytic_id (str): Identifier of the analytic area
            gate_id (str): Identifier of the gate to get data from
            end_date (datetime): End date for the data retrieval (UTC)
            days (int, optional): Number of days to look back from end_date. Defaults to 1.

        Returns:
            list[DistributionCount]: List of records containing timestamp and vehicle counts by type

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> distribution = wt.flow.get_historical_distribution_data(
            ...     analytic_id="test-id",
            ...     gate_id="test-id",
            ...     end_date=datetime(2023, 1, 1),
            ...     days=1
            ... )
        """
        from_datetime = get_start_date(end_date=end_date, days=days)
        to_datetime = dt.combine(end_date, time.max)  # 23:59:59.999999
        response = self.client.send_flow_data_management_api_request(
            path="data",
            params={
                "area": self.area_id,
                "analytics": analytic_id,
                "gate_id": gate_id,
                "value_type": "distribution",
                "from_datetime": convert_datetime_to_iso_str(from_datetime),
                "to_datetime": convert_datetime_to_iso_str(to_datetime),
            },
        )
        result = [DistributionCount(**dict(zip(DISTRIBUTION_COLUMNS, row))) for row in response]
        return result
