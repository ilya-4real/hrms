from dataclasses import dataclass
from typing import Sequence, override

from domain.entities.employee import Employee, WorkLocation, Workload
from domain.entities.kpi import KPIRecord
from domain.interfaces import EmployeeGateway, KPIGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class AddEmlpoyeeCommand(BaseCommand):
    first_name: str
    second_name: str
    job_title: str
    salary: int
    award: int
    department_id: str
    email: str
    sm_link: str
    workload: Workload
    work_location: WorkLocation


@dataclass
class AddEmployeeUseCase(BaseUseCase[AddEmlpoyeeCommand, Employee]):
    gateway: EmployeeGateway
    db_session: DBSession

    @override
    async def execute(self, command: AddEmlpoyeeCommand) -> Employee:
        new_employee = Employee(
            command.first_name,
            command.second_name,
            command.job_title,
            command.salary,
            command.award,
            command.department_id,
            email_address=command.email,
            sm_link=command.sm_link,
            work_location=command.work_location,
            workload=command.workload,
        )
        await self.gateway.add_employee(new_employee)
        await self.db_session.commit()
        return new_employee


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


@dataclass
class GetEmployeesByDepartmentCommand(BaseCommand):
    department_id: str
    limit: int
    offset: int


@dataclass
class GetEmployeesByDepartmentUseCase(
    BaseUseCase[GetEmployeesByDepartmentCommand, Sequence[Employee]]
):
    gateway: EmployeeGateway
    db_session: DBSession

    @override
    async def execute(
        self, command: GetEmployeesByDepartmentCommand
    ) -> Sequence[Employee]:
        employees = await self.gateway.get_employees_by_department(
            command.department_id, command.limit, command.offset
        )
        await self.db_session.rollback()
        return employees


@dataclass
class UpdateEmployeeCommand(BaseCommand):
    employee_oid: str
    first_name: str
    second_name: str
    job_title: str
    salary: int
    award: int
    department_id: str
    email: str
    sm_link: str
    workload: Workload
    work_location: WorkLocation
    kpi_value: int


@dataclass
class UpdateEmployeeUsecase(BaseUseCase[UpdateEmployeeCommand, Employee]):
    employee_gateway: EmployeeGateway
    kpi_gateway: KPIGateway
    db_session: DBSession

    @override
    async def execute(self, command: UpdateEmployeeCommand) -> Employee:
        # employee = Employee(**asdict(command))
        employee = Employee(
            oid=command.employee_oid,
            first_name=command.first_name,
            second_name=command.second_name,
            job_title=command.job_title,
            salary=command.salary,
            award=command.award,
            department_id=command.department_id,
            email_address=command.email,
            sm_link=command.sm_link,
            workload=command.workload,
            work_location=command.work_location
        )
        kpi_record = KPIRecord(command.kpi_value, command.employee_oid)
        await self.employee_gateway.update_employee(employee)
        await self.kpi_gateway.upsert_kpi_value(kpi_record)
        await self.db_session.commit()
        return employee
