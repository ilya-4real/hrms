from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.department import Department
from domain.entities.employee import Employee
from domain.entities.event import Event
from domain.entities.kpi import KPIRecord


class BaseGateway(ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session


class DepartmentGateway(BaseGateway):
    @abstractmethod
    async def create_department(self, department: Department): ...

    @abstractmethod
    async def get_all_departments(self) -> Sequence[Department]: ...

    @abstractmethod
    async def get_department_detail(self, department_id: str): ...


class EmployeeGateway(BaseGateway):
    @abstractmethod
    async def add_employee(self, employee: Employee) -> Employee: ...

    @abstractmethod
    async def get_all_employees(self, limit=0, offset=10) -> Sequence[Employee]: ...

    @abstractmethod
    async def get_employee_detail(self, employee_id: str) -> Employee: ...

    @abstractmethod
    async def get_employees_by_department(
        self, department_oid: str, limit=0, offset=10
    ) -> Sequence[Employee]: ...

    @abstractmethod
    async def update_employee(self, employee: Employee) -> Employee: ...


class KPIGateway(BaseGateway):
    @abstractmethod
    async def upsert_kpi_value(self, kpi_record: KPIRecord) -> None: ...

    @abstractmethod
    async def get_kpi_of_employee(self, employee_id: str) -> list[KPIRecord]: ...


class EventGateway(BaseGateway):
    @abstractmethod
    async def create_event(self, event: Event) -> Event: ...

    @abstractmethod
    async def get_current_events(self) -> list[Event]: ...

    @abstractmethod
    async def delete_event(self, event_oid: str) -> None: ...

    @abstractmethod
    async def get_events_history(
        self, limit: int = 0, offset: int = 10
    ) -> list[Event]: ...


class StatsGateway(BaseGateway):
    @abstractmethod
    async def get_count_by_department(self) -> dict[str, int]:
        ...

    @abstractmethod
    async def get_employees_stats(self) -> dict[str, int]:
        ...
