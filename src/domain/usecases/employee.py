from dataclasses import dataclass
from typing import Sequence, override

from domain.entities.employee import Employee, WorkLocation, Workload
from domain.interfaces import EmployeeGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class AddEmlpoyeeCommand(BaseCommand):
    first_name: str
    second_name: str
    job_title: str
    salary: int
    award: int
    department_id: str
    workload: Workload
    work_location: WorkLocation


@dataclass
class AddEmployeeUseCase(BaseUseCase[AddEmlpoyeeCommand, None]):
    gateway: EmployeeGateway
    db_session: DBSession

    @override
    async def execute(self, command: AddEmlpoyeeCommand) -> None:
        new_employee = Employee(
            command.first_name,
            command.second_name,
            command.job_title,
            command.salary,
            command.award,
            command.department_id,
            command.work_location,
            command.workload,
        )
        await self.gateway.add_employee(new_employee)
        await self.db_session.commit()


@dataclass
class GetAllEmployeesCommand(BaseCommand):
    offset: int
    limit: int


@dataclass
class GetAllEmployeesUseCase(BaseUseCase[GetAllEmployeesCommand, Sequence[Employee]]):
    gateway: EmployeeGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetAllEmployeesCommand) -> Sequence[Employee]:
        employees = await self.gateway.get_all_employees(command.limit, command.offset)
        await self.db_session.rollback()
        return employees

@dataclass
class GetEmployeeCommand(BaseCommand):
    employee_id: str


@dataclass
class GetEmployeeUsecase(BaseUseCase[GetEmployeeCommand, Employee]):
    gateway: EmployeeGateway
    db_session: DBSession
    
    @override
    async def execute(self, command: GetEmployeeCommand) -> Employee:
        employee = await self.gateway.get_employee_detail(command.employee_id)
        await self.db_session.rollback()
        return employee

