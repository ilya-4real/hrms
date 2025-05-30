from typing import Annotated
from fastapi import APIRouter, Form, Query, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.templating import Jinja2Templates

from application.api.v1.employees.schemas import EmployeeSchema, UpdateEmployeeschema
from application.api.v1.utils import Paginator
from domain.usecases.employee import (
    AddEmployeeUseCase,
    AddEmlpoyeeCommand,
    GetAllEmployeesCommand,
    GetAllEmployeesUseCase,
    GetEmployeeCommand,
    GetEmployeeUsecase,
    UpdateEmployeeCommand,
    UpdateEmployeeUsecase,
)
from domain.usecases.kpi import GetEmployeesKPIList, GetEmployeesKPIListUseCase


router = APIRouter(route_class=DishkaRoute, tags=["employees"], prefix="/employees")


@router.get("/page")
async def get_employees_page(request: Request, templ: FromDishka[Jinja2Templates]):
    return templ.TemplateResponse(request, "employees_page.html")


@router.post("")
async def add_employee(
    request: Request,
    employee: Annotated[EmployeeSchema, Form()],
    usecase: FromDishka[AddEmployeeUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = AddEmlpoyeeCommand(**employee.model_dump())
    created_employee = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "employee_card.html", context={"employee": created_employee}
    )


@router.get("")
async def get_all_employees(
    request: Request,
    paginator: Annotated[Paginator, Query()],
    usecase: FromDishka[GetAllEmployeesUseCase],
    templ: FromDishka[Jinja2Templates],
):
    limit, offset = paginator.get_limit_and_offset()
    next_page = paginator.page + 1
    command = GetAllEmployeesCommand(offset, limit)
    employees = await usecase.execute(command)
    print(employees)
    return templ.TemplateResponse(
        request,
        "employee_list.html",
        context={"employees": employees, "next_page": next_page},
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


@router.get("/{employee_id}/update_form")
async def get_update_form(
    employee_id: str,
    request: Request,
    templ: FromDishka[Jinja2Templates],
    usecase: FromDishka[GetEmployeeUsecase],
):
    print("requested to update employee with id", employee_id)
    command = GetEmployeeCommand(employee_id)

    employee = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "employee_update_form.html", {"employee": employee}
    )


@router.put("/{employee_id}")
async def update_employee(
    employee_id: str,
    employee: Annotated[UpdateEmployeeschema, Form()],
    request: Request,
    usecase: FromDishka[UpdateEmployeeUsecase],
    templ: FromDishka[Jinja2Templates],
):
    command = UpdateEmployeeCommand(employee_id, **employee.model_dump())
    empl = await usecase.execute(command)
    return templ.TemplateResponse(request, "employee_detail.html", {"employee": empl})


@router.get("/{employee_id}/kpi")
async def get_employee_kpi_history(
    request: Request,
    employee_id: str,
    usecase: FromDishka[GetEmployeesKPIListUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetEmployeesKPIList(employee_id)
    log = await usecase.execute(command)
    months_names = [month.strftime("%B") for month in log.months]
    print(months_names)
    return templ.TemplateResponse(
        request,
        "employee_kpi_chart.html",
        context={"months": months_names, "values": log.values},
    )
