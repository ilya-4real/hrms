from typing import override
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from domain.entities.kpi import KPIRecord
from domain.interfaces import KPIGateway
from gateways.postgres.models.kpi_records import KPIRecordORM


class SQLKPIGateway(KPIGateway):
    async def upsert_kpi_value(self, kpi_record: KPIRecord) -> None:
        stmt = pg_insert(KPIRecordORM).values(
            oid=kpi_record.oid,
            date_added=kpi_record.last_date,
            employee_oid=kpi_record.employee_id,
            value=kpi_record.value,
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["date_added", "employee_oid"],
            set_={"value": stmt.excluded.value},
        )
        await self.db_session.execute(stmt)

    @override
    async def get_kpi_of_employee(self, employee_id: str) -> list[KPIRecord]:
        query = (
            select(KPIRecordORM)
            .where(KPIRecordORM.employee_oid == employee_id)
            .order_by(KPIRecordORM.date_added.desc())
        )
        result = await self.db_session.execute(query)
        records = result.scalars().all()
        return [record.to_entity() for record in records]
