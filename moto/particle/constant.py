from datetime import datetime
import hashlib
import pytz # type: ignore

SECOND = 1 
TIME_UNIT_TABLE = {
	"second": SECOND,
	"minute": SECOND * 60,
	"hour": SECOND * 60 * 60,
	"day": SECOND * 60 * 60 * 24,
	"week": SECOND * 60 * 60 * 24 * 7,
	"month": SECOND * 60 * 60 * 24 * 30,
	"year": SECOND * 60 * 60 * 24 * 365,
}

TIMEZONE_TABLE = {
    timezone: int(
        pytz.timezone(timezone).utcoffset(datetime.now()).total_seconds() / 3600
    )
    for timezone in pytz.all_timezones
}

HASH_ALGORITHMS = {
    algo: hashlib.new(algo) for algo in hashlib.algorithms_available
}

for i in HASH_ALGORITHMS:
	print(i)

