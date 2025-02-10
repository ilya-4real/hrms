from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol, TypeVar


@dataclass
class BaseCommand(ABC):
    pass


CT = TypeVar("CT", bound=BaseCommand)
RT = TypeVar("RT", bound=Any)


@dataclass
class BaseUseCase[CT, RT](ABC):
    @abstractmethod
    async def execute(self, command: CT) -> RT: ...


class DBSession(Protocol):
    @abstractmethod
    async def commit(self): ...
    @abstractmethod
    async def flush(self): ...
    @abstractmethod
    async def rollback(self):...
