from typing import Annotated
from fastapi import APIRouter, Form, Query, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.templating import Jinja2Templates

from application.api.v1.employees.schemas import AddEmployeeSchema
from application.api.v1.utils import Paginator
from domain.usecases.employee import (
    AddEmployeeUseCase,
    AddEmlpoyeeCommand,
    GetAllEmployeesCommand,
    GetAllEmployeesUseCase,
    GetEmployeeCommand,
    GetEmployeeUsecase,
)


router = APIRouter(route_class=DishkaRoute, tags=["employees"], prefix="/employees")


@router.post("")
async def add_employee(
    employee: Annotated[AddEmployeeSchema, Form()],
    usecase: FromDishka[AddEmployeeUseCase],
):
    command = AddEmlpoyeeCommand(**employee.model_dump())
    await usecase.execute(command)


@router.get("")
async def get_all_employees(
    request: Request,
    paginator: Annotated[Paginator, Query()],
    usecase: FromDishka[GetAllEmployeesUseCase],
    templ: FromDishka[Jinja2Templates],
):
    limit, offset = paginator.get_limit_and_offset()
    command = GetAllEmployeesCommand(offset, limit)
    employees = await usecase.execute(command)
    print(employees)
    return templ.TemplateResponse(
        request, "employees.html", context={"employees": employees}
    )


@router.get("/{employee_id}")
async def get_employee_detail(
    employee_id: str,
    request: Request,
    usecase: FromDishka[GetEmployeeUsecase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetEmployeeCommand(employee_id)
    employee = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "employee_detail.html", context={"employee": employee}
    )
