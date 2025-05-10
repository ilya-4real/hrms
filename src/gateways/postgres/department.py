from typing import Sequence, override

from sqlalchemy.orm import selectinload
from domain.entities.department import Department
from domain.interfaces import DepartmentGateway
from gateways.postgres.models.department import DepartmentORM
from sqlalchemy import select

from gateways.postgres.models.employee import EmployeeOrm


class SQLDepartmentGateway(DepartmentGateway):
    @override
    async def create_department(self, department: Department):
        self.db_session.add(DepartmentORM.from_entity(department))

    @override
    async def get_all_departments(self) -> Sequence[Department]:
        query = select(DepartmentORM).options(selectinload(DepartmentORM.employees))
        result = await self.db_session.execute(query)
        res = result.scalars().all()
        return [department.to_entity() for department in res]

    @override
    async def get_department_detail(self, department_id: str) -> Department:
        query = (
            select(DepartmentORM)
            .where(DepartmentORM.oid == department_id)
            .options(selectinload(DepartmentORM.employees))
        )
        result = await self.db_session.execute(query)
        department = result.scalar_one()
        return department.to_entity()
