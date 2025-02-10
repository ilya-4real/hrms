from typing import Sequence, override
from domain.entities.department import Department
from domain.interfaces import DepartmentGateway
from gateways.postgres.models.department import DepartmentORM
from sqlalchemy import select


class SQLDepartmentGateway(DepartmentGateway):
    @override
    async def create_department(self, department: Department):
        self.db_session.add(DepartmentORM.from_entity(department))

    @override
    async def get_all_departments(self) -> Sequence[Department]:
        query = select(DepartmentORM)
        result = await self.db_session.execute(query)
        res = result.scalars().all()
        return [department.to_entity() for department in res]

    @override
    async def get_department_detail(self, department_id: str): ...
