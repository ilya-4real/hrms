from typing import Annotated
from fastapi import APIRouter, Form

from application.api.v1.events.schemas import CreateEventShema


router = APIRouter(prefix="/events", tags=["events"])

@router.post("")
async def create_new_event(event: Annotated[CreateEventShema, Form()]):
    return

@router.get("/current")
async def get_current_events():
    return "here it is"
