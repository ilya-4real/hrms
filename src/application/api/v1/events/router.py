from typing import Annotated
from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates

from application.api.v1.events.schemas import CreateEventShema
from application.api.v1.utils import Paginator
from domain.usecases.event import (
    CreateEventCommand,
    CreateEventUseCase,
    DeleteEventCommand,
    DeleteEventUsecase,
    GetCurrentEvents,
    GetCurrentEventsUseCase,
    GetEventsHistoryCommand,
    GetEventsHistoryUseCase,
)


router = APIRouter(route_class=DishkaRoute, prefix="/events", tags=["events"])


@router.post("")
async def create_new_event(
    request: Request,
    event: Annotated[CreateEventShema, Form()],
    usecase: FromDishka[CreateEventUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = CreateEventCommand(event.title, event.starts_at)
    new_event = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "event_card.html", context={"event": new_event}
    )


@router.get("/current")
async def get_current_events(
    request: Request,
    usecase: FromDishka[GetCurrentEventsUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetCurrentEvents()
    events = await usecase.execute(command)
    return templ.TemplateResponse(
        request, "events_list.html", context={"events": events}
    )

@router.get("/history_page")

async def get_events_history_page(
    request: Request,
    templ: FromDishka[Jinja2Templates],
):
    return templ.TemplateResponse(request, "events_history.html")


@router.get("/")
async def get_events_history(
    request: Request,
    paginator: Annotated[Paginator, Query()],
    usecase: FromDishka[GetEventsHistoryUseCase],
    templ: FromDishka[Jinja2Templates],
):
    command = GetEventsHistoryCommand(*paginator.get_limit_and_offset())
    events = await usecase.execute(command)
    return templ.TemplateResponse(
        request,
        "events_list.html",
        context={"events": events, "loadable": True, "next_page": paginator.page + 1},
    )


@router.delete("/{event_oid}")
async def delet_event(event_oid: str, usecase: FromDishka[DeleteEventUsecase]) -> None:
    command = DeleteEventCommand(event_oid)
    await usecase.execute(command)
