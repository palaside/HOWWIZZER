import pytest
from datetime import date
from backend.services.business_day_engine import (
    is_business_day,
    get_adjusted_cycle_date,
    get_weekly_submission_date,
    get_next_business_day,
    get_weekly_cycle_range
)

def test_weekend_detection():
    # 2026-10-17 is Saturday, 2026-10-18 is Sunday
    assert is_business_day(date(2026, 10, 17)) is False
    assert is_business_day(date(2026, 10, 18)) is False
    # 2026-10-16 is Friday
    assert is_business_day(date(2026, 10, 16)) is True

def test_thai_holiday_detection():
    # 2026-10-13 is King Bhumibol Memorial Day (National Holiday)
    assert is_business_day(date(2026, 10, 13)) is False

def test_roll_backward_holiday_adjustment():
    # If target is Tuesday 2026-10-13 (Holiday), roll backward should land on Monday 2026-10-12
    adjusted = get_adjusted_cycle_date(date(2026, 10, 13), direction='backward')
    assert adjusted == date(2026, 10, 12)

def test_weekly_submission_date_is_thursday_and_never_friday():
    # Friday 2026-06-19 -> baseline submission must be Thursday 2026-06-18
    sub_date = get_weekly_submission_date(date(2026, 6, 19))
    assert sub_date == date(2026, 6, 18)
    assert sub_date.weekday() == 3  # Thursday (0=Mon, 1=Tue, 2=Wed, 3=Thu)
    assert is_business_day(sub_date) is True

def test_weekly_submission_date_holiday_rollback():
    # If Thursday is a holiday (2026-12-10 Constitution Day), Friday is 2026-12-11
    # Submission date must roll back to Wednesday 2026-12-09 (and never Friday 11th)
    sub_date = get_weekly_submission_date(date(2026, 12, 11))
    assert sub_date == date(2026, 12, 9)
    assert sub_date.weekday() == 2  # Wednesday
    assert is_business_day(sub_date) is True

def test_weekly_cycle_range_normal():
    # Friday 2026-10-16 is a normal working day
    res = get_weekly_cycle_range(date(2026, 10, 16))
    assert res["start_date"] == "2026-10-12"
    assert res["end_date"] == "2026-10-16"
    assert res["range_text"] == "12 - 16 ต.ค. 69"
    assert res["target_date_thai"] == "16/10/69"
    assert res["is_friday_holiday"] is False

def test_weekly_cycle_range_holiday_rollback():
    # Friday 2026-10-23 is Chulalongkorn Day (National Holiday)
    # The weekly cycle must roll back to Thursday 2026-10-22: '19 - 22 ต.ค. 69'
    res = get_weekly_cycle_range(date(2026, 10, 23))
    assert res["start_date"] == "2026-10-19"
    assert res["end_date"] == "2026-10-22"
    assert res["range_text"] == "19 - 22 ต.ค. 69"
    assert res["target_date_thai"] == "23/10/69"
    assert res["is_friday_holiday"] is True

