from __future__ import annotations

import random
from typing import TYPE_CHECKING

from pydenim.misc.constants import WALL_ID, OBSTACLE_ID, SPACE_ID, FOOD_CHANCE, EGG_LIFESPAN
from pydenim.objects.base import BoardActor, Creatable, StaticActor
from pydenim.services import id_generator

if TYPE_CHECKING:
    from pydenim.genetics.gene import Genome
    from pydenim.objects.organism import Organism, Bio


class Egg(StaticActor, Creatable):
    priority = 2

    def __init__(self, id: int, child_genome: Genome, child_bio: Bio, lifespan: int):
        self.id = id
        self.child_genome = child_genome
        self.child_bio = child_bio
        self.lifespan = lifespan
        super().__init__(id)

    def age(self) -> BoardActor:
        return Egg(self.id, self.child_genome, self.child_bio, self.lifespan - 1) if self.lifespan > 0 else self.birth()

    @classmethod
    def new(cls, child_genome: Genome, child_bio: Bio) -> Egg:
        return Egg(id_generator(), child_genome, child_bio, EGG_LIFESPAN)

    def birth(self) -> Organism:
        return Organism.new(self.child_genome, self.child_bio)


class Food(StaticActor):

    def __init__(self, id: int, lifespan: int, value: int):
        self.id = id
        self.lifespan = lifespan
        self.value = value
        super().__init__(id)

    def age(self) -> BoardActor:
        return Food(self.id, self.lifespan - 1, self.value) if self.lifespan > 0 else SPACE


class Wall(StaticActor):
    pass


class Obstacle(StaticActor):
    pass


class Space(StaticActor):
    priority = 1

    def age(self) -> BoardActor:
        lifespan = 10
        value = 5
        return Food(id_generator(), lifespan, value) if random.random() < FOOD_CHANCE else self


WALL = Wall(id=WALL_ID)
OBSTACLE = Obstacle(id=OBSTACLE_ID)
SPACE = Space(id=SPACE_ID)
