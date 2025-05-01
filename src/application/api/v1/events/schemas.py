from datetime import datetime
from pydantic import BaseModel


class CreateEventShema(BaseModel):
    title: str
    starts_at: datetime
