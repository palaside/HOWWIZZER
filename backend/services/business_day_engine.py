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

THAI_MONTHS_SHORT = [
    "", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
]

def get_weekly_cycle_range(target_date: date) -> dict:
    """
    Computes the weekly cycle date range (Monday to Friday or adjusted for holidays).
    - Monday of the week is start date.
    - Friday of the week is baseline end date.
    - If Friday is a holiday/non-business day, rolls backward to the last business day of the week (e.g. Thursday).
    - Formats Thai Buddhist era string: e.g. '12 - 16 ต.ค. 69' or '12 - 15 ต.ค. 69'.
    """
    monday = target_date - timedelta(days=target_date.weekday())
    friday = monday + timedelta(days=4)
    
    end_date = friday
    while end_date > monday and not is_business_day(end_date):
        end_date -= timedelta(days=1)
        
    end_b_year = (end_date.year + 543) % 100
    start_day = str(monday.day)
    end_day = str(end_date.day)
    
    if monday.month == end_date.month and monday.year == end_date.year:
        range_text = f"{start_day} - {end_day} {THAI_MONTHS_SHORT[end_date.month]} {end_b_year:02d}"
    else:
        range_text = f"{start_day} {THAI_MONTHS_SHORT[monday.month]} - {end_day} {THAI_MONTHS_SHORT[end_date.month]} {end_b_year:02d}"
        
    target_b_year = (target_date.year + 543) % 100
    target_date_thai = f"{target_date.day:02d}/{target_date.month:02d}/{target_b_year:02d}"
    
    sub_date = get_weekly_submission_date(friday)
    sub_b_year = (sub_date.year + 543) % 100
    sub_date_thai = f"{sub_date.day} {THAI_MONTHS_SHORT[sub_date.month]} {sub_b_year:02d}"

    return {
        "target_date_iso": target_date.isoformat(),
        "target_date_thai": target_date_thai,
        "start_date": monday.isoformat(),
        "end_date": end_date.isoformat(),
        "range_text": range_text,
        "submission_date": sub_date.isoformat(),
        "submission_date_thai": sub_date_thai,
        "is_friday_holiday": not is_business_day(friday),
        "friday_date": friday.isoformat()
    }
