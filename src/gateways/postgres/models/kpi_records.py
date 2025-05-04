from datetime import date
from sqlalchemy import Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from domain.entities.kpi import KPIRecord
from gateways.postgres.base import BaseORM


class KPIRecordORM(BaseORM):
    __tablename__ = "kpi_records"
    __table_args__ = (
        UniqueConstraint("date_added", "employee_oid", name="unique_date_employee_kpi"),
    )

    oid: Mapped[str] = mapped_column(primary_key=True)
    date_added: Mapped[date] = mapped_column(Date)
    value: Mapped[int] = mapped_column()
    employee_oid: Mapped[str] = mapped_column(ForeignKey("employees.oid"))

    employee: Mapped["EmployeeOrm"] = relationship(back_populates="kpi_records")  # noqa: F821

    def to_entity(self) -> KPIRecord:
        return KPIRecord(self.value, self.employee_oid, self.date_added, oid=self.oid)
