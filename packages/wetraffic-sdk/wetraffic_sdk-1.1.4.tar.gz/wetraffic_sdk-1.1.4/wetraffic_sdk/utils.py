from datetime import datetime, time, timedelta

from .exceptions import TooManyDaysError


def convert_datetime_to_iso_str(datetime_object: datetime) -> str:
    iso_formatted = datetime_object.isoformat(timespec="milliseconds")
    return iso_formatted.replace("+00:00", "Z")


def get_start_date(*, end_date: datetime, days: int, max_days: int = 15) -> datetime:
    is_in_interval = 1 <= days <= max_days
    if not is_in_interval:
        raise TooManyDaysError(f"Days must be between 1 and {max_days}, provided days: " + str(days))
    return datetime.combine(end_date - timedelta(days=min(days - 1, max_days)), time.min)  # 00:00:00
