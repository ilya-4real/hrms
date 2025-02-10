from typing import Annotated
from fastapi import APIRouter, Form, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.templating import Jinja2Templates

from domain.usecases.department import (
    CreateDeaprtmentCommand,
    CreateDeaprtmentUseCase,
    GetAllDepartmentsUseCase,
    GetAllDepartmentsCommand,
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
    usecase: FromDishka[CreateDeaprtmentUseCase],
):
    command = CreateDeaprtmentCommand(department_name)
    await usecase.execute(command)


@router.get("/{department_id}")
async def get_department_detail(department_id: str): ...
