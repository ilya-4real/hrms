from dataclasses import dataclass

from domain.entities.event import Event
from domain.usecases.base import BaseCommand, BaseUseCase


@dataclass
class CreateEventCommand(BaseCommand):
    event: Event


@dataclass
class CreateEventUseCase(BaseUseCase): ...
