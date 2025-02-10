from dataclasses import dataclass, field
from enum import Enum

from domain.entities.base import BaseEntity


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
    work_location: WorkLocation = field(default=WorkLocation.Office)
    workload: Workload = field(default=Workload.Fulltime)
