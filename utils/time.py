from datetime import datetime, timezone, timedelta

# Singapore timezone (UTC+8)
SINGAPORE_TZ = timezone(timedelta(hours=8))

def get_singapore_time():
    return datetime.now(timezone.utc).astimezone(SINGAPORE_TZ)

def format_singapore_time_for_filename():
    return get_singapore_time().strftime("%Y-%m-%d_%H-%M-%S")

def format_singapore_datetime_for_report():
    return get_singapore_time().strftime("%Y/%m/%d %H:%M:%S (SGT)")
