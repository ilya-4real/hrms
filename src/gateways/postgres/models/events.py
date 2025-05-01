
from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from gateways.postgres.base import BaseORM


class Event(BaseORM):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(100), primary_key=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
