from dataclasses import dataclass
from typing import Sequence, override
from domain.entities.department import Department
from domain.interfaces import DepartmentGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class CreateDeaprtmentCommand(BaseCommand):
    name: str


@dataclass
class CreateDeaprtmentUseCase(BaseUseCase[CreateDeaprtmentCommand, None]):
    department_gateway: DepartmentGateway
    db_session: DBSession

    @override
    async def execute(self, command: CreateDeaprtmentCommand) -> None:
        new_department = Department(command.name)
        await self.department_gateway.create_department(new_department)
        await self.db_session.commit()


@dataclass
class GetAllDepartmentsCommand(BaseCommand): ...


@dataclass
class GetAllDepartmentsUseCase(
    BaseUseCase[GetAllDepartmentsCommand, Sequence[Department]]
):
    department_gateway: DepartmentGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetAllDepartmentsCommand) -> Sequence[Department]:
        return await self.department_gateway.get_all_departments()
