from datetime import datetime, timezone

DEFAULT_TIMEZONE = timezone.utc


def set_default_timezone(date: datetime) -> datetime:
    """Set the default timezone for datetime library."""
    return datetime(
        date.year,
        date.month,
        date.day,
        date.hour,
        date.minute,
        date.second,
        date.microsecond,
        tzinfo=DEFAULT_TIMEZONE,
    )
