from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Tuple


class BoardActor(metaclass=ABCMeta):

    def __init__(self, id: int):
        self.id = id

    def __hash__(self):
        return self.id

    def __eq__(self, other: BoardActor):
        return isinstance(other, BoardActor) and self.id == other.id

    @property
    @abstractmethod
    def interacts(self) -> bool:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    @abstractmethod
    def age(self) -> BoardActor:
        pass

    @abstractmethod
    def interact(self, other: BoardActor) -> Tuple[BoardActor, BoardActor]:
        pass


class StaticActor(BoardActor):
    interacts = False
    priority = 0

    def age(self) -> BoardActor:
        return self

    def interact(self, other: BoardActor) -> Tuple[BoardActor, BoardActor]:
        return self, other


class DynamicActor(BoardActor, metaclass=ABCMeta):
    interacts = True


class Creatable(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def new(cls, *args, **kwargs) -> BoardActor:
        pass
