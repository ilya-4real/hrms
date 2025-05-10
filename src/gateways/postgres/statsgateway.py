from typing import override

from sqlalchemy import func, select
from domain.interfaces import StatsGateway
from gateways.postgres.models.department import DepartmentORM
from gateways.postgres.models.employee import EmployeeOrm


class SQLStatsGateway(StatsGateway):
    @override
    async def get_count_by_department(self) -> dict[str, int]:
        query = (
            select(DepartmentORM.name, func.count(EmployeeOrm.oid))
            .join(EmployeeOrm, DepartmentORM.oid == EmployeeOrm.department_id, isouter=True)
            .group_by(DepartmentORM.name)
        )

        result = await self.db_session.execute(query)
        stats = {}
        for department_name, cnt in result:
            stats[department_name] = cnt
        return stats

    @override
    async def get_company_stats(self) -> dict[str, int]:
        subquery = select(func.count(DepartmentORM.oid)).scalar_subquery()
        query = select(
            subquery.label("Departments count"),
            func.count(EmployeeOrm.oid).label("Employee headcount"),
            func.count().filter(EmployeeOrm.workload == "Fulltime").label("Fulltime employees"),
            func.count().filter(EmployeeOrm.work_location == "Remote").label("Remote employees"),
        )

        result = await self.db_session.execute(query)
        statistics = {}
        for key, value in zip(result.keys(), result.one()):
            statistics[key] = value
        return statistics

