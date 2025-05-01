
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from domain.entities.event import Event
from gateways.postgres.base import BaseORM


class EventORM(BaseORM):
    __tablename__ = "events"

    oid: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    @classmethod
    def from_entity(cls, event: Event) -> "EventORM":
        return EventORM(oid=event.oid, title=event.title, starts_at=event.starts_at)

    def to_entity(self) -> Event:
        return Event(self.title, self.starts_at, oid=self.oid)
