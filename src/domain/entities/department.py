from dataclasses import dataclass
from domain.entities.base import BaseEntity


@dataclass
class Department(BaseEntity):
    name: str
