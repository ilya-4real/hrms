from dataclasses import dataclass
from typing import override
from domain.interfaces import StatsGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class GetCountByDepartment(BaseCommand): ...


@dataclass
class GetCountByDepartmentUseCase(BaseUseCase):
    stats_gateway: StatsGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetCountByDepartment) -> dict[str, int]:
        result = await self.stats_gateway.get_count_by_department()
        await self.db_session.rollback()
        return result

@dataclass
class GetCompanyStats(BaseCommand): ...


@dataclass
class GetCompanyStatsUsecase(BaseUseCase):
    stats_gateway: StatsGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetCompanyStats) -> dict[str, int]:
        result =  await self.stats_gateway.get_company_stats()
        await self.db_session.rollback()
        return result
