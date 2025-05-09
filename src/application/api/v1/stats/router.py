from fastapi import APIRouter, Request
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.templating import Jinja2Templates

from domain.usecases.stats import GetCountByDepartment, GetCountByDepartmentUseCase


router = APIRouter(route_class=DishkaRoute, prefix="/statistics", tags=["statistics"])


@router.get("/employee_count")
async def employee_count_by_department(
    request: Request,
    usecase: FromDishka[GetCountByDepartmentUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetCountByDepartment()
    result = await usecase.execute(command)
    department_names = list(result.keys())
    counts = list(result.values())
    return templ.TemplateResponse(
        request,
        "headcount_chart.html",
        context={"department_names": department_names, "counts": counts},
    )
