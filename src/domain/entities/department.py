from dataclasses import dataclass, field

from domain.entities.base import BaseEntity
from domain.entities.employee import Employee


@dataclass
class Department(BaseEntity):
    name: str
    employees: list[Employee] = field(default_factory=list)

    def add_employee(self, employee: Employee) -> None:
        self.employees.append(employee)
