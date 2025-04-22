from pydantic import BaseModel, EmailStr, Field

from domain.entities.employee import WorkLocation, Workload



class EmployeeSchema(BaseModel):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    email: EmailStr
    sm_link: str
    department_id: str
    salary: int = Field(ge=0)
    award: int = Field(ge=0)
    work_location: WorkLocation = Field(default=WorkLocation.Office)
    workload: Workload = Field(default=Workload.Fulltime)


class UpdateEmployeeschema(BaseModel):
    job_title: str = Field(min_length=1)
    first_name: str
    second_name: str
    email: EmailStr
    sm_link: str
    department_id: str
    salary: int = Field(ge=0)
    award: int = Field(ge=0)
    kpi_value: int
    work_location: WorkLocation = Field(default=WorkLocation.Office)
    workload: Workload = Field(default=Workload.Fulltime)
