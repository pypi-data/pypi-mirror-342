from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, validate_call

from .api_client import ApiClient
from .logging_config import setup_logger
from .utils import convert_datetime_to_iso_str, get_start_date

logger = setup_logger()

TRAFFIC_COLUMNS = [
    "datetime",
    "length_in_meters",
    "travel_time_in_seconds",
    "traffic_delay_in_seconds",
    "traffic_length_in_meters",
    "no_traffic_travel_time_in_seconds",
    "historic_traffic_travel_time_in_seconds",
    "live_traffic_incidents_travel_time_in_seconds",
    "delta",
]

traffic_index = {key: index for index, key in enumerate(TRAFFIC_COLUMNS)}


class TrafficData(BaseModel):
    datetime: datetime
    length_in_meters: int
    travel_time_in_seconds: int
    traffic_delay_in_seconds: int
    traffic_length_in_meters: int
    no_traffic_travel_time_in_seconds: int
    historic_traffic_travel_time_in_seconds: int
    live_traffic_incidents_travel_time_in_seconds: int


class StreetsGeoJsonProperties(BaseModel):
    name: Optional[str] = Field(default=None, description="Street name")
    frc: int = Field(ge=0, le=8, description="Functional Road Class")
    hash: str = Field(description="Street hash (identifier)")


class StreetsGeoJsonGeometry(BaseModel):
    type: Literal["LineString"]
    coordinates: list[list[float]]


class StreetsGeoJsonFeature(BaseModel):
    type: Literal["Feature"]
    properties: StreetsGeoJsonProperties
    geometry: StreetsGeoJsonGeometry


class StreetsGeoJson(BaseModel):
    type: Literal["FeatureCollection"]
    features: list[StreetsGeoJsonFeature]


class RealTimeMap:
    """
    Interface for interacting with real-time map data
    """

    def __init__(self, *, client: ApiClient):
        self.client = client
        self.area_id = self.client.area_id

    @validate_call
    def get_geohash_list(self) -> list[str]:
        """
        Get the geohash list for an area

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> geohash_list = wt.real_time_map.get_geohash_list()

        Returns:
           list[str]: geohash list
        """
        return self.client.get_asset_from_features_bucket(path=f"{self.area_id}/polylines/index.json")

    @validate_call
    def get_streets(self, *, geohash: str) -> StreetsGeoJson:
        """
        Get the streets for a specific geohash

        Args:
            geohash (str): geohash

        Returns:
            StreetsGeoJson: streets

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> streets = wt.real_time_map.get_streets(geohash="test-geohash")
            >>> # Returns a StreetsGeoJson object (geoJSON):
        """
        raw_streets = self.client.get_asset_from_features_bucket(path=f"{self.area_id}/polylines/{geohash}.json")
        return StreetsGeoJson(
            type="FeatureCollection",
            features=[StreetsGeoJsonFeature(type="Feature", **feature) for feature in raw_streets],
        )

    @validate_call
    def get_traffic_loads(self, *, year: int) -> list[datetime]:
        """
        Get the load dates for traffic

        Args:
            year (int): year

        Returns:
            list[datetime]: date list

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.real_time_map.get_traffic_loads(year=2023)
            >>> # Returns a list of datetime objects:
            >>> # [datetime(2023, 1, 1, 0, 0), datetime(2023, 1, 2, 0, 0)]
        """
        response = self.client.invoke_rpc(
            action="get_traffic_loads", params={"area_type": f"{self.area_id}-tomtom-routing", "month": str(year)}
        )
        return [datetime.fromisoformat(date_str) for date_str in response]

    @validate_call
    def get_traffic_data(self, *, end_date: datetime, geohash: str, hash: str, days: int = 1) -> list[TrafficData]:
        """
        Get the traffic data for a specific street

        Args:
            end_date (datetime): end date
            geohash (str): geohash
            hash (str): hash
            days (int): days

        Returns:
            list[TrafficData]: traffic data

        Example:
            >>> from wetraffic_sdk import WetrafficSdk
            >>> wt = WetrafficSdk(area="area01")
            >>> loads = wt.real_time_map.get_traffic_data(end_date=datetime(2023, 1, 1), geohash="test-geohash", hash="test-hash")
            >>> # Returns a list of TrafficData objects:
            >>> # [TrafficData(datetime=datetime(2023, 1, 1, 0, 0), length_in_meters=10, travel_time_in_seconds=10)]
        """
        start_date = get_start_date(end_date=end_date, days=days)
        data = self.client.invoke_rpc(
            action="get_traffic_data",
            params={
                "geohash": geohash,
                "hash": hash,
                "min_datetime": convert_datetime_to_iso_str(start_date),
                "max_datetime": convert_datetime_to_iso_str(end_date),
            },
        )
        result = [TrafficData(**dict(zip(TRAFFIC_COLUMNS, row))) for row in data]
        return result
