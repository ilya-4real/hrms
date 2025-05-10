from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM as PGENUM

from domain.entities.department import Department
from domain.entities.employee import Employee, WorkLocation, Workload
from gateways.postgres.base import BaseORM
from gateways.postgres.models.kpi_records import KPIRecordORM



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
    current_kpi: Mapped[int] = mapped_column(default=0)
    hire_date: Mapped[date] = mapped_column(Date())
    email_address: Mapped[str] = mapped_column(String(50), unique=True)
    sm_link: Mapped[str] = mapped_column(unique=True)
    department_id: Mapped[str] = mapped_column(ForeignKey("departments.oid"))

    department: Mapped["DepartmentORM"] = relationship(back_populates="employees")  # type: ignore  # noqa: F821
    kpi_records: Mapped["KPIRecordORM"] = relationship(back_populates="employee")


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
            email_address=entity.email_address,
            sm_link=entity.sm_link,
            hire_date=entity.hire_date
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
            email_address=self.email_address,
            sm_link=self.sm_link,
            department_id=self.department_id,
            department=Department(self.department.name, oid=self.department_id),
            current_kpi=self.current_kpi
        )
