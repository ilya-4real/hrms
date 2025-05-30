from dataclasses import dataclass
from datetime import datetime
from typing import override

from domain.entities.event import Event
from domain.interfaces import EventGateway
from domain.usecases.base import BaseCommand, BaseUseCase, DBSession


@dataclass
class CreateEventCommand(BaseCommand):
    title: str
    starts_at: datetime


@dataclass
class CreateEventUseCase(BaseUseCase):
    event_gateway: EventGateway
    db_session: DBSession

    @override
    async def execute(self, command: CreateEventCommand) -> Event:
        event = Event(command.title, command.starts_at)
        event = await self.event_gateway.create_event(event)
        await self.db_session.commit()
        return event


@dataclass
class GetCurrentEvents(BaseCommand): ...


@dataclass
class GetCurrentEventsUseCase(BaseUseCase):
    event_gateway: EventGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetCurrentEvents) -> list[Event]:
        events = await self.event_gateway.get_current_events()
        print(events)
        await self.db_session.rollback()
        return events


@dataclass
class DeleteEventCommand(BaseCommand):
    event_oid: str


@dataclass
class DeleteEventUsecase(BaseUseCase):
    event_gateway: EventGateway
    db_session: DBSession

    @override
    async def execute(self, command: DeleteEventCommand) -> None:
        await self.event_gateway.delete_event(command.event_oid)
        await self.db_session.commit()


@dataclass
class GetEventsHistoryCommand(BaseCommand):
    limit: int
    offset: int


@dataclass
class GetEventsHistoryUseCase(BaseUseCase):
    event_gateway: EventGateway
    db_session: DBSession

    @override
    async def execute(self, command: GetEventsHistoryCommand) -> list[Event]:
        events = await self.event_gateway.get_events_history(
            command.limit, command.offset
        )
        await self.db_session.rollback()
        return events
