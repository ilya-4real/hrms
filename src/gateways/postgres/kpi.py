from datetime import date

from sqlalchemy.dialects.postgresql import insert as pg_insert

from domain.interfaces import KPIGateway
from gateways.postgres.models.kpi_records import KPIRecord


class SQLKPIGateway(KPIGateway):
    async def upsert_kpi_value(self, employee_id: str, kpi_value: int) -> None:
        date_added = date(date.today().year, date.today().month, 1)
        stmt = pg_insert(KPIRecord).values(
            date_added=date_added, employee_oid=employee_id, value=kpi_value
        )
    
        stmt = stmt.on_conflict_do_update(index_elements=['date_added'], set_={"value": stmt.excluded.value})
        await self.db_session.execute(stmt)
