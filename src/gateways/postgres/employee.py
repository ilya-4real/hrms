from typing import Sequence, override
from domain.entities.employee import Employee
from domain.interfaces import EmployeeGateway
from gateways.postgres.models.employee import EmployeeOrm
from sqlalchemy import select


class SQLEmployeeGateway(EmployeeGateway):
    @override
    async def add_employee(self, employee: Employee):
        self.db_session.add(EmployeeOrm.from_entity(employee))

    @override
    async def get_all_employees(self, limit=0, offset=10) -> Sequence[Employee]:
        query = select(EmployeeOrm).limit(limit).offset(offset)
        db_answer = await self.db_session.execute(query)
        orm_employees = db_answer.scalars().all()
        return [employee.to_entity() for employee in orm_employees]

    @override
    async def get_employee_detail(self, employee_id: str) -> Employee:
        employee = await self.db_session.get_one(EmployeeOrm, ident=employee_id)
        return employee.to_entity()
