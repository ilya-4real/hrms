from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.department import Department
from domain.entities.employee import Employee


class DepartmentGateway(ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    @abstractmethod
    async def create_department(self, department: Department): ...

    @abstractmethod
    async def get_all_departments(self) -> Sequence[Department]: ...

    @abstractmethod
    async def get_department_detail(self, department_id: str): ...


class EmployeeGateway(ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

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


class KPIGateway(ABC):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    @abstractmethod
    async def upsert_kpi_value(self, employee_id: str, kpi_value: int) -> None: ...
