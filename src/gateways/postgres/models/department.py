from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.entities.department import Department
from gateways.postgres.base import BaseORM
from gateways.postgres.models.employee import EmployeeOrm


class DepartmentORM(BaseORM):
    __tablename__ = "departments"
    oid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    employees: Mapped[list["EmployeeOrm"]] = relationship(back_populates="department")

    @classmethod
    def from_entity(cls, department: Department) -> "DepartmentORM":
        return DepartmentORM(oid=department.oid, name=department.name)

    def to_entity(self) -> Department:
        return Department(self.name, oid=self.oid)
