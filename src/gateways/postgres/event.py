from datetime import datetime
from typing import override

from sqlalchemy import Date, asc, cast, select
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
