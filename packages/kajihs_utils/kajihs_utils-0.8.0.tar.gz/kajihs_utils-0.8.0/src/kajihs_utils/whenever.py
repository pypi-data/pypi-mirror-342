"""Utils for better date and times, specifically using whenever."""

from datetime import datetime
from whenever import LocalDateTime, ZonedDateTime, Instant, OffsetDateTime, SystemDateTime

type ExactDateTime = ZonedDateTime | Instant | OffsetDateTime | SystemDateTime

type AllDateTime = LocalDateTime | ExactDateTime


def dt_to_system_datetime(dt: datetime) -> SystemDateTime:
    """Convert into exact time by assuming system timezone if necessary."""
    return (
        LocalDateTime.from_py_datetime(dt).assume_system_tz()
        if dt.tzinfo is None
        else SystemDateTime.from_py_datetime(dt)
    )
