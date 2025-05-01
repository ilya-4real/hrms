
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from domain.entities.event import Event
from gateways.postgres.base import BaseORM


class EventORM(BaseORM):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(100), primary_key=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @classmethod
    def from_entity(cls, event: Event) -> "EventORM":
        return EventORM(title=event.title, starts_at=event.starts_at)

    def to_entity(self) -> Event:
        return Event(self.title, self.starts_at)
