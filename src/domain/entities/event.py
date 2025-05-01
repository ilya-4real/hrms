from dataclasses import dataclass
from datetime import datetime
from domain.entities.base import BaseEntity


@dataclass
class Event(BaseEntity):
    title: str
    starts_at: datetime
