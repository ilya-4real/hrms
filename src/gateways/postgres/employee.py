from dataclasses import asdict
from typing import Sequence, override
from domain.entities.employee import Employee
from domain.interfaces import EmployeeGateway
from gateways.postgres.models.employee import EmployeeOrm
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload, selectinload


class SQLEmployeeGateway(EmployeeGateway):
    @override
    async def add_employee(self, employee: Employee) -> Employee:
        self.db_session.add(EmployeeOrm.from_entity(employee))
        return employee

    @override
    async def get_all_employees(self, limit=0, offset=10) -> Sequence[Employee]:
        query = (
            select(EmployeeOrm)
            .limit(limit)
            .offset(offset)
            .options(selectinload(EmployeeOrm.department))
        )
        db_answer = await self.db_session.execute(query)
        orm_employees = db_answer.scalars().all()
        return [employee.to_entity() for employee in orm_employees]

    @override
    async def get_employee_detail(self, employee_id: str) -> Employee:
        employee = await self.db_session.get_one(
            EmployeeOrm, ident=employee_id, options=[joinedload(EmployeeOrm.department)]
        )
        return employee.to_entity()

    async def get_employees_by_department(self, department_oid: str, limit=0, offset=10) -> Sequence[Employee]:
        query = (
            select(EmployeeOrm)
            .where(EmployeeOrm.department_id == department_oid)
            .limit(limit)
            .offset(offset)
            .options(selectinload(EmployeeOrm.department))
        )
        db_answer = await self.db_session.execute(query)
        orm_employees = db_answer.scalars().all()
        return [employee.to_entity() for employee in orm_employees]

    async def update_employee(self, employee: Employee) -> Employee:
        print(asdict(employee))
        stmt = update(EmployeeOrm).where(EmployeeOrm.oid == employee.oid).values(
            first_name=employee.first_name,
            second_name=employee.second_name,
            job_title=employee.job_title,
            department_id=employee.department_id,
            email_address=employee.email_address,
            sm_link=employee.sm_link,
            salary=employee.salary,
            award=employee.award,
            workload=employee.workload,
            work_location=employee.work_location,
            current_kpi=employee.current_kpi
        )
        await self.db_session.execute(stmt)
        return employee
