import pytz
from datetime import datetime, timedelta

from illex.decorators.function import function


@function("date")
def handle_date(fmt: str) -> str:
    tz = pytz.timezone("America/Sao_Paulo")
    now = datetime.now(tz)
    dates = {
        "today": now.strftime("%d/%m/%Y"),
        "now": now.strftime("%d/%m/%Y %H:%M"),
        "yesterday": (now - timedelta(1)).strftime("%d/%m/%Y"),
        "tomorrow": (now + timedelta(1)).strftime("%d/%m/%Y"),
    }
    try:
        return dates.get(fmt, now.strftime(fmt))
    except ValueError:
        return "[Invalid date format]"