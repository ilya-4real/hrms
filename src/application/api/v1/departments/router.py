from typing import Annotated
from fastapi import APIRouter, Form, Query, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.templating import Jinja2Templates

from application.api.v1.utils import Paginator
from domain.usecases.department import (
    CreateDeaprtmentCommand,
    CreateDeaprtmentUseCase,
    GetAllDepartmentsUseCase,
    GetAllDepartmentsCommand,
)
from domain.usecases.employee import (
    GetEmployeesByDepartmentCommand,
    GetEmployeesByDepartmentUseCase,
)

router = APIRouter(route_class=DishkaRoute, prefix="/departments", tags=["departments"])


@router.get("")
async def get_departments(
    request: Request,
    usecase: FromDishka[GetAllDepartmentsUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetAllDepartmentsCommand()
    deps = await usecase.execute(command)
    print(deps[0])
    return templ.TemplateResponse(
        request, "departments.html", context={"departments": deps}
    )


@router.get("/options")
async def get_departments_options(
    request: Request,
    usecase: FromDishka[GetAllDepartmentsUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetAllDepartmentsCommand()
    deps = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "departments_options.html", context={"departments": deps}
    )


@router.post("")
async def create_deaprtment(
    department_name: Annotated[str, Form()],
    request: Request,
    usecase: FromDishka[CreateDeaprtmentUseCase],
    templ: FromDishka[Jinja2Templates]
):
    command = CreateDeaprtmentCommand(department_name)
    department = await usecase.execute(command)
    return templ.TemplateResponse(request, "department_card.html", context={"department": department})



@router.get("/{department_id}/employees")
async def get_department_employees(
    department_id: str,
    paginator: Annotated[Paginator, Query()],
    request: Request,
    usecase: FromDishka[GetEmployeesByDepartmentUseCase],
    templ: FromDishka[Jinja2Templates],
):
    limit, offset = paginator.get_limit_and_offset()
    command = GetEmployeesByDepartmentCommand(department_id, limit, offset)
    employees = await usecase.execute(command)
    print(employees)
    return templ.TemplateResponse(
        request, "employee_list.html", context={"employees": employees}
    )
