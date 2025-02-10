from pydantic import BaseModel, Field

from domain.entities.employee import WorkLocation, Workload



class AddEmployeeSchema(BaseModel):
    first_name: str = Field(min_length=1)
    second_name: str = Field(min_length=1)
    job_title: str = Field(min_length=1)
    department_id: str
    salary: int = Field(ge=0)
    award: int = Field(ge=0)
    work_location: WorkLocation = Field(default=WorkLocation.Office)
    workload: Workload = Field(default=Workload.Fulltime)
