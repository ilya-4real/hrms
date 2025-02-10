from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM as PGENUM

from domain.entities.employee import Employee, WorkLocation, Workload
from gateways.postgres.base import BaseORM


class EmployeeOrm(BaseORM):
    __tablename__ = "employees"
    oid: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    workload: Mapped[Workload] = mapped_column(
        PGENUM(Workload), nullable=False, default=Workload.Fulltime
    )
    work_location: Mapped[WorkLocation] = mapped_column(
        PGENUM(WorkLocation), nullable=False, default=WorkLocation.Office
    )
    job_title: Mapped[str] = mapped_column(String(50))
    salary: Mapped[int]
    award: Mapped[int]
    department_id: Mapped[str] = mapped_column(ForeignKey("departments.oid"))

    department: Mapped["DepartmentORM"] = relationship(back_populates="employees")  # type: ignore  # noqa: F821

    @classmethod
    def from_entity(cls, entity: Employee) -> "EmployeeOrm":
        return EmployeeOrm(
            oid=entity.oid,
            first_name=entity.first_name,
            second_name=entity.second_name,
            workload=entity.workload,
            job_title=entity.job_title,
            work_location=entity.work_location,
            salary=entity.salary,
            award=entity.award,
            department_id=entity.department_id,
        )
    
    def to_entity(self) -> Employee:
        return Employee(
            oid=self.oid,
            first_name=self.first_name,
            second_name=self.second_name,
            workload=self.workload,
            job_title=self.job_title,
            work_location=self.work_location,
            salary=self.salary,
            award=self.award,
            department_id=self.department_id,
        )
