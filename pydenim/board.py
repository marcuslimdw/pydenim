from __future__ import annotations

from operator import attrgetter
from typing import List, Tuple, Union

from pydenim.config import Config
from pydenim.misc.data_structures import Sliceable2DList
from pydenim.misc.functional import choice
from pydenim.objects.base import BoardActor, DynamicActor
from pydenim.objects.neutral import SPACE, WALL
from pydenim.objects.organism import Organism

# This should be handled with a parametrised type, but it didn't really work out.
PositionedDynamicActor = Tuple[int, int, DynamicActor]
PositionedBoardActor = Tuple[int, int, BoardActor]


class Board:

    def __init__(self, config: Config, actors: Sliceable2DList[BoardActor], epoch: int = 0):
        self.config = config
        self.actors = actors
        self.epoch = epoch

    def __iter__(self):
        return iter(self.actors)

    def __getitem__(self, coordinates: Tuple[Union[int, slice], Union[int, slice]]):
        return self.actors[coordinates]

    def age(self) -> Board:
        new_actors = self.actors.map(lambda actor: actor.age())
        removed_actors = set()
        for p_actor, p_neighbour in self._get_interacting_pairs(new_actors):
            actor_x, actor_y, actor = p_actor
            neighbour_x, neighbour_y, neighbour = p_neighbour
            old_ids = {actor.id, neighbour.id}
            if old_ids & removed_actors:
                break

            new_actor, new_neighbour = actor.interact(neighbour)
            new_ids = {new_actor.id, new_neighbour.id}
            for id in old_ids - new_ids:
                removed_actors.add(id)

            new_actors[actor_x, actor_y] = new_actor
            new_actors[neighbour_x, neighbour_y] = new_neighbour

        return Board(self.config, new_actors, self.epoch + 1)

    @classmethod
    def initialise(cls, config: Config) -> Board:
        actors = Sliceable2DList.uniform(config.n_rows, config.n_cols, WALL)
        actors.inner.fill(SPACE)

        starting_organisms = cls._generate_starting_organisms()
        for organism in starting_organisms:
            actors.inner.inner = organism

        return cls(config, actors, 0)

    def _get_interacting_pairs(self, actors: Sliceable2DList[BoardActor]):
        active_actors = ((x, y, actor) for x, y, actor in actors.iter_coords() if actor.interacts)
        actors_by_priority = (obj for *_, obj in sorted(active_actors, key=attrgetter('priority'), reverse=True))
        neighbours = (self._get_neighbour(x, y) for x, y, _ in active_actors)
        return zip(actors_by_priority, neighbours)

    @staticmethod
    def _generate_starting_organisms() -> List[Organism]:
        pass

    @staticmethod
    def _add_obstacles_and_organisms(actors: Sliceable2DList, row_size: int):
        pass

    def _get_neighbour(self, x: int, y: int) -> PositionedBoardActor:
        x, y = choice([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
        return x, y, self[x, y]
