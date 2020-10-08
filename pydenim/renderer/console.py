from typing import Mapping, Type

from pydenim.board import Board
from pydenim.objects.base import BoardActor
from pydenim.objects.neutral import Egg, Food, Obstacle, Space, Wall
from pydenim.objects.organism import Organism
from pydenim.renderer.base import Renderer


class ConsoleRenderer(Renderer):
    _RENDER_MAP: Mapping[Type[BoardActor], str] = {
        Wall    : '█',
        Obstacle: '█',
        Space   : ' ',
        Egg     : 'O',
        Food    : '*',
        Organism: 'x'
    }

    def render_board(self, board: Board):
        print('\n'.join(''.join(self.convert_actor(obj) for obj in row) for row in board))

    def render_actor(self, obj: BoardActor):
        print(self.convert_actor(obj))

    def render_text(self, text: str):
        print(text)

    def convert_actor(self, obj: BoardActor):
        return self._RENDER_MAP[type(obj)]
