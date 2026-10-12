import json
from pathlib import Path
from datetime import date, timedelta

HOLIDAYS_FILE = Path(__file__).parent.parent / "data" / "thai_holidays.json"

def load_thai_holidays() -> set[date]:
    if not HOLIDAYS_FILE.exists():
        return set()
    with open(HOLIDAYS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    holidays = set()
    for year, h_list in data.items():
        for item in h_list:
            holidays.add(date.fromisoformat(item["date"]))
    return holidays

_CACHED_HOLIDAYS = load_thai_holidays()

def is_business_day(target_date: date) -> bool:
    """Returns True if the target_date is Monday-Friday and NOT a Thai public holiday."""
    if target_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
        return False
    if target_date in _CACHED_HOLIDAYS:
        return False
    return True

def get_adjusted_cycle_date(target_date: date, direction: str = "backward") -> date:
    """Rolls forward or backward until a valid business day is reached."""
    step = timedelta(days=-1 if direction == "backward" else 1)
    current = target_date
    while not is_business_day(current):
        current += step
    return current

def get_weekly_submission_date(cycle_friday: date) -> date:
    """
    Computes the official memo submission date for a weekly inspection cycle.
    RULE-PROD-DOC-ENGINE-V1 (Rule 6):
    - Baseline is Thursday (1 day before Friday).
    - Strictly rolls backward if Thursday is a public holiday.
    - Must be between Monday and Thursday.
    - NEVER lands on Friday, weekend, or holiday.
    - Stamped identically on memo header and bottom-right 'พิมพ์/ทาน' block.
    """
    candidate = cycle_friday - timedelta(days=1)
    while not is_business_day(candidate) or candidate.weekday() >= 4:
        candidate -= timedelta(days=1)
    return candidate

def get_next_business_day(target_date: date) -> date:
    """Returns the subsequent valid business day."""
    current = target_date + timedelta(days=1)
    while not is_business_day(current):
        current += timedelta(days=1)
    return current
