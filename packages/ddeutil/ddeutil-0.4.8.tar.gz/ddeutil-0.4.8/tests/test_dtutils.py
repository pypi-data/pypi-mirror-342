from datetime import datetime
from unittest import mock

import ddeutil.core.dtutils as dtutils
import pytest
from dateutil.relativedelta import relativedelta
from ddeutil.core.dtutils import (
    DatetimeDim,
    calc_date_freq,
    closest_quarter,
    last_dom,
    next_date,
    next_date_freq,
)
from freezegun import freeze_time


def test_dt_dimension():
    assert 6 == DatetimeDim.get_dim("year")

    with pytest.raises(ValueError):
        DatetimeDim.get_dim("date_of_month")


def test_get_date():
    assert datetime.now(tz=dtutils.LOCAL_TZ).date() == dtutils.get_date("date")

    with freeze_time("2024-01-01 01:00:00"):
        assert datetime(
            2024,
            1,
            1,
            1,
        ).replace(
            tzinfo=dtutils.LOCAL_TZ
        ) == dtutils.get_date("datetime", _tz=dtutils.LOCAL_TZ)

        assert datetime(
            2024,
            1,
            1,
            1,
        ).replace(
            tzinfo=dtutils.LOCAL_TZ
        ) == dtutils.get_date("datetime", _tz="UTC")

        assert "20240101010000" == dtutils.get_date("%Y%m%d%H%M%S")


def test_next_date():
    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            next_date(datetime(2024, 1, 1), mode="day")

    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="day") == datetime(
        2023, 2, 1, 0, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="month") == datetime(
        2023, 2, 28, 0, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="hour") == datetime(
        2023, 1, 31, 1, 0
    )
    assert next_date(datetime(2023, 1, 31, 0, 0, 0), mode="year") == datetime(
        2024, 1, 31, 0, 0
    )


def test_closest_quarter():
    assert closest_quarter(datetime(2024, 9, 25)) == datetime(2024, 9, 30, 0, 0)
    assert closest_quarter(datetime(2024, 2, 13)) == datetime(
        2023, 12, 31, 0, 0
    )


def test_last_dom():
    assert last_dom(datetime(2024, 2, 29)) == datetime(2024, 2, 29, 0, 0)
    assert last_dom(
        datetime(2024, 1, 31) + relativedelta(months=1)
    ) == datetime(2024, 2, 29, 0, 0)
    assert last_dom(
        datetime(2024, 2, 29) + relativedelta(months=1)
    ) == datetime(2024, 3, 31, 0, 0)


def test_replace_date():
    assert datetime(2023, 1, 31, 0, 0) == dtutils.replace_date(
        datetime(2023, 1, 31, 13, 2, 47),
        mode="day",
    )

    assert datetime(2023, 1, 1, 0, 0) == dtutils.replace_date(
        datetime(2023, 1, 31, 13, 2, 47),
        mode="year",
    )


def test_next_date_freq():
    assert next_date_freq(datetime(2024, 1, 3), freq="D") == datetime(
        2024, 1, 4, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 1, 3), freq="D", prev=True
    ) == datetime(2024, 1, 2, 0, 0)
    assert next_date_freq(datetime(2024, 1, 3), freq="W") == datetime(
        2024, 1, 10, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 1, 3), freq="W", prev=True
    ) == datetime(2023, 12, 27, 0, 0)
    assert next_date_freq(datetime(2024, 1, 3), freq="M") == datetime(
        2024, 2, 3, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 31), freq="M") == datetime(
        2024, 2, 29, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 17), freq="Q") == datetime(
        2024, 4, 17, 0, 0
    )
    assert next_date_freq(datetime(2024, 1, 31), freq="Q") == datetime(
        2024, 4, 30, 0, 0
    )
    assert next_date_freq(datetime(2025, 12, 31), freq="Q") == datetime(
        2026, 3, 31, 0, 0
    )
    assert next_date_freq(datetime(2024, 5, 21), freq="Y") == datetime(
        2025, 5, 21, 0, 0
    )
    assert next_date_freq(datetime(2024, 5, 31), freq="Y") == datetime(
        2025, 5, 31, 0, 0
    )
    assert next_date_freq(
        datetime(2024, 5, 31), freq="Y", prev=True
    ) == datetime(2023, 5, 31, 0, 0)

    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            next_date_freq(datetime(2024, 5, 31), freq="Y", prev=True)


def test_calc_data_freq():
    assert calc_date_freq(datetime(2024, 1, 13), freq="D") == datetime(
        2024, 1, 13, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 3), freq="W") == datetime(
        2024, 1, 3, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 3), freq="M") == datetime(
        2023, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 31), freq="M") == datetime(
        2024, 1, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 1, 31), freq="Q") == datetime(
        2023, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2025, 12, 31), freq="Q") == datetime(
        2025, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 12, 31), freq="Y") == datetime(
        2024, 12, 31, 0, 0
    )
    assert calc_date_freq(datetime(2024, 5, 31), freq="Y") == datetime(
        2023, 12, 31, 0, 0
    )

    with mock.patch("ddeutil.core.dtutils.relativedelta", None):
        with pytest.raises(ImportError):
            calc_date_freq(datetime(2024, 5, 31), freq="Y")
