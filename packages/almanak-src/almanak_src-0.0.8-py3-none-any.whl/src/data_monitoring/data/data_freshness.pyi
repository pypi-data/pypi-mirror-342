import datetime
from typing import Iterable

ENABLE_FRESHNESS_CHECK: bool

def current_data_date(instruments: Iterable[str]) -> dict[str, dict[str, datetime.datetime]]:
    """Returns the latest data date for given instruments using the Timestamp_dt column."""
