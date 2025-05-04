from dataclasses import dataclass
from typing import override
from domain.entities.kpi import KPILog, KPIRecord
from domain.interfaces import KPIGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class GetEmployeesKPIList(BaseCommand):
    employee_id: str


@dataclass
class GetEmployeesKPIListUseCase(BaseUseCase):
    kpi_gateway: KPIGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetEmployeesKPIList) -> KPILog:
        records = await self.kpi_gateway.get_kpi_of_employee(command.employee_id)
        await self.db_session.rollback()
        log = KPILog(records)
        records = log.build()
        print(records)
        return log

