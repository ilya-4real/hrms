from dataclasses import dataclass, field
from datetime import date
from enum import Enum

from domain.entities.base import BaseEntity
from domain.entities.department import Department


class Workload(Enum):
    Fulltime = "fulltime"
    Parttime = "parttime"

class WorkLocation(Enum):
    Office = "office"
    Remote = "remote"
    Hybrid = "hybrid"


@dataclass
class Employee(BaseEntity):
    first_name: str
    second_name: str
    job_title: str
    salary: int
    award: int
    department_id: str
    email_address: str 
    sm_link: str 
    current_kpi: int = field(default=0)
    hire_date: date = field(default_factory=date.today)
    department: Department | None = field(default=None)
    work_location: WorkLocation = field(default=WorkLocation.Office)
    workload: Workload = field(default=Workload.Fulltime)
