from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from application.api.v1.events.schemas import CreateEventShema
from domain.usecases.event import CreateEventCommand, CreateEventUseCase, GetCurrentEvents, GetCurrentEventsUseCase


router = APIRouter(route_class=DishkaRoute, prefix="/events", tags=["events"])


@router.post("")
async def create_new_event(
    event: Annotated[CreateEventShema, Form()], usecase: FromDishka[CreateEventUseCase]
):
    command = CreateEventCommand(event.title, event.starts_at)
    new_event = await usecase.execute(command)
    print(event)
    return str(new_event)


@router.get("/current")
async def get_current_events(request: Request, usecase: FromDishka[GetCurrentEventsUseCase], templ: FromDishka[Jinja2Templates]):
    command = GetCurrentEvents()
    events = await usecase.execute(command)
    return templ.TemplateResponse(request, "events_list.html", context={"events": events})

