from datetime import date
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from gateways.postgres.base import BaseORM


class KPIRecord(BaseORM):
    __tablename__ = "kpi_records"

    date_added: Mapped[date] = mapped_column(Date, primary_key=True)
    value: Mapped[int] = mapped_column()
    employee_oid: Mapped[str] = mapped_column(ForeignKey("employees.oid"))

    employee: Mapped["EmployeeOrm"] = relationship(back_populates="kpi_records")
