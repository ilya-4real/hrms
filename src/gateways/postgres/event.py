from datetime import datetime
from typing import override

from sqlalchemy import Date, asc, cast, delete, select
from domain.entities.event import Event
from domain.interfaces import EventGateway
from gateways.postgres.models.events import EventORM


class SQLEventGateway(EventGateway):
    @override
    async def get_current_events(self) -> list[Event]:
        today = datetime.now().date()
        query = (
            select(EventORM)
            .where(cast(EventORM.starts_at, Date) == today)
            .order_by(asc(EventORM.starts_at))
        )
        result = await self.db_session.execute(query)
        events = result.scalars().all()
        return [event.to_entity() for event in events]

    @override
    async def create_event(self, event: Event) -> Event:
        self.db_session.add(EventORM.from_entity(event))
        return event

    @override
    async def delete_event(self, event_oid: str) -> None:
        stmt = delete(EventORM).where(EventORM.oid == event_oid)
        await self.db_session.execute(stmt)

    @override
    async def get_events_history(self, limit: int = 0, offset: int = 10) -> list[Event]:
        query = select(EventORM).order_by(EventORM.starts_at).limit(limit).offset(offset)
        result = await self.db_session.execute(query)
        events_orm = result.scalars().all()
        return [event.to_entity() for event in events_orm]
