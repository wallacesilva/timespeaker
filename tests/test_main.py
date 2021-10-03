from datetime import datetime

import pytest

from timespeaker.main import PeriodNotFound, validate_period


@pytest.fixture
def datetime_now():
    return datetime(2022, 1, 25, 13, 0, 0)


def test_validate_period_each_hour(datetime_now):

    is_valid = validate_period(
        name="hour",
        time_now=datetime_now,
        last_time_run=datetime_now.replace(hour=datetime_now.hour - 1),
    )

    assert is_valid is True


def test_validate_period_each_halfhour(datetime_now):
    datetime_now = datetime_now.replace(minute=30)

    is_valid = validate_period(
        name="halfhour",
        time_now=datetime_now,
        last_time_run=datetime_now.replace(hour=datetime_now.hour - 1),
    )

    assert is_valid is True


def test_validate_period_each_5_minutes(datetime_now):
    datetime_now = datetime_now.replace(minute=5)

    is_valid = validate_period(
        name="5_min",
        time_now=datetime_now,
        last_time_run=datetime_now.replace(hour=datetime_now.hour - 1),
    )

    assert is_valid is True


def test_validate_period_for_invalid_period(datetime_now):

    with pytest.raises(PeriodNotFound):
        validate_period(
            name="invalid",
            time_now=datetime_now,
            last_time_run=datetime_now.replace(hour=datetime_now.hour - 1),
        )
