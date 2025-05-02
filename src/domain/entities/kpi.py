from dataclasses import dataclass, field
from datetime import date
from collections import deque

from domain.entities.base import BaseEntity


def first_day_of_this_month() -> date:
    today = date.today()
    return date(today.year, today.month, 1)


@dataclass
class KPIRecord(BaseEntity):
    value: int | None
    employee_id: str
    last_date: date = field(default_factory=lambda: first_day_of_this_month())


@dataclass
class KPILog:
    records: list[KPIRecord]

    def build(self) -> list[KPIRecord]:
        timeline: list[KPIRecord] = []
        last_date = self.records[0].last_date
        employee_id = self.records[0].employee_id
        dates_sequence = deque(KPILog.get_timeline(last_date))
        while dates_sequence:
            actual = self.records.pop()
            should_be = dates_sequence.pop()
            if actual.last_date == should_be:
                timeline.append(actual)
            else:
                self.records.append(actual)
                timeline.append(KPIRecord(None, employee_id, should_be))
        return timeline

    @staticmethod
    def get_timeline(last_date: date) -> list[date]:
        timeline: list[date] = []
        for i in range(12):
            cur_date = KPILog.substract_months(last_date, i)
            timeline.append(cur_date)
        return timeline

    @staticmethod
    def substract_months(cur_date: date, months: int) -> date:
        year = cur_date.year
        month = cur_date.month - (months % 12)

        if month <= 0:
            year -= 1
            month += 12

        return cur_date.replace(year, month, 1)
