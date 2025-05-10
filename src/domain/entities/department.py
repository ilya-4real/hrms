from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from domain.entities.base import BaseEntity

if TYPE_CHECKING:
    from domain.entities.employee import Employee


@dataclass
class Department(BaseEntity):
    name: str
    employees: list["Employee"] = field(default_factory=list)
