from datetime import datetime
import pytz # type: ignore

TIME_UNIT_TABLE = {
    "second": 1,
    "minute": 60,
    "hour": 3600,
    "day": 86400,
    "week": 604800,
    "month": 2592000,
    "year": 31536000,
}

TIMEZONE_TABLE = {
    timezone: int(
        pytz.timezone(timezone).utcoffset(datetime.now()).total_seconds() / 3600
    )
    for timezone in pytz.all_timezones
}
