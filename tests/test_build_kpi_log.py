from datetime import date
from domain.entities.kpi import KPILog, KPIRecord


def test_substract_months_with_year_change():
    last_date = date(2025, 1, 1)
    correct = date(2024, 12, 1)

    assert KPILog.substract_months(last_date, 1) == correct


def test_substract_months_without_year_change():
    last_date = date(2025, 2, 1)
    correct = date(2025, 1, 1)

    assert KPILog.substract_months(last_date, 1) == correct


def test_build_timeline_with_year_change():
    last_date = date(2025, 2, 1)
    correct = [
        date(2025, 2, 1),
        date(2025, 1, 1),
        date(2024, 12, 1),
        date(2024, 11, 1),
        date(2024, 10, 1),
        date(2024, 9, 1),
        date(2024, 8, 1),
        date(2024, 7, 1),
        date(2024, 6, 1),
        date(2024, 5, 1),
        date(2024, 4, 1),
        date(2024, 3, 1),
    ]

    built = KPILog.get_timeline(last_date)
    assert len(built) == 12
    assert built == correct


def test_build_timeline_without_year_change():
    last_date = date(2024, 12, 1)
    correct = [
        date(2024, 12, 1),
        date(2024, 11, 1),
        date(2024, 10, 1),
        date(2024, 9, 1),
        date(2024, 8, 1),
        date(2024, 7, 1),
        date(2024, 6, 1),
        date(2024, 5, 1),
        date(2024, 4, 1),
        date(2024, 3, 1),
        date(2024, 2, 1),
        date(2024, 1, 1),
    ]

    built = KPILog.get_timeline(last_date)
    assert len(built) == 12
    assert built == correct


def test_build_log():
    records = [KPIRecord(1, "some_id", date(2025, 2, 1))]

    log = KPILog(records)
    built = log.build()
    should_be = [
        KPIRecord(None, "some_id", date(2024, 3, 1)),
        KPIRecord(None, "some_id", date(2024, 4, 1)),
        KPIRecord(None, "some_id", date(2024, 5, 1)),
        KPIRecord(None, "some_id", date(2024, 6, 1)),
        KPIRecord(None, "some_id", date(2024, 7, 1)),
        KPIRecord(None, "some_id", date(2024, 8, 1)),
        KPIRecord(None, "some_id", date(2024, 9, 1)),
        KPIRecord(None, "some_id", date(2024, 10, 1)),
        KPIRecord(None, "some_id", date(2024, 11, 1)),
        KPIRecord(None, "some_id", date(2024, 12, 1)),
        KPIRecord(None, "some_id", date(2025, 1, 1)),
        KPIRecord(1, "some_id", date(2025, 2, 1)),
    ]

    assert len(built) == 12
    for b, s in zip(built, should_be):
        assert b.value == s.value
        assert b.employee_id == s.employee_id
        assert b.last_date == s.last_date
