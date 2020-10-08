from abc import ABCMeta, abstractmethod

from pydenim.board import Board
from pydenim.objects.base import BoardActor


class Renderer(metaclass=ABCMeta):

    @abstractmethod
    def render_board(self, board: Board):
        pass

    @abstractmethod
    def render_actor(self, actor: BoardActor):
        pass

    @abstractmethod
    def convert_actor(self, actor: BoardActor):
        pass

    @abstractmethod
    def render_text(self, text: str):
        pass
