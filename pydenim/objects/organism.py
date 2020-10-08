from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from random import random
from typing import Callable, Optional, Set, TYPE_CHECKING, Tuple, Union, cast

from pydenim.misc.constants import IGNORE_CHANCE, MATE_CHANCE
from pydenim.misc.functional import attrgettern, either, orc
from pydenim.misc.internal_types import Gender
from pydenim.objects.base import BoardActor, Creatable, DynamicActor
from pydenim.objects.neutral import OBSTACLE, SPACE, WALL
from pydenim.services import id_generator

if TYPE_CHECKING:
    from pydenim.genetics.gene import Genome
    from pydenim.objects.neutral import Food, Space, Egg


class Organism(DynamicActor, Creatable):
    active = True

    def __init__(self, id: int, genome: Genome, statistics: Statistics, bio: Bio, effects: Effects,
                 pregnant_with: Optional[Egg]):
        self.genome = genome
        self.statistics = statistics
        self.bio = bio
        self.effects = effects
        self.pregnant_with = pregnant_with
        super().__init__(id)

    @property
    def priority(self) -> int:
        return self.statistics.agility

    @classmethod
    def new(cls, genome: Genome, bio: Bio) -> Organism:
        return Organism(id_generator(), genome, genome.generate_statistics(), bio, set(), None)

    def age(self) -> BoardActor:
        return self

    def interact(self, other: BoardActor) -> Tuple[BoardActor, BoardActor]:
        # I miss pattern matching.
        if other is SPACE:
            if self.pregnant_with:
                return self.modify(pregnant_with=None), self.pregnant_with

            return either((cast(BoardActor, self), other), (other, self))

        elif other in {WALL, OBSTACLE}:
            return self, other

        elif isinstance(other, Food):
            return self._eat(other)

        elif isinstance(other, Organism):
            return self._interact_organism(other)

        else:
            raise TypeError(other)

    def modify(self, genome: Optional[Genome] = None, statistics: Optional[Statistics] = None,
               bio: Optional[Bio] = None, effects: Optional[Effects] = None, pregnant_with: Optional[Egg] = None):
        return Organism(self.id, orc(genome, self.genome), orc(statistics, self.statistics), orc(bio, self.bio),
                        orc(effects, self.effects), orc(pregnant_with, self.pregnant_with))

    def _eat(self, other: Food) -> Tuple[Space, Organism]:
        new_self = self.modify(statistics=self.statistics.modify(health=lambda health: health + other.value))
        return SPACE, new_self

    def _interact_organism(self, other: Organism) -> Tuple[BoardActor, BoardActor]:
        action_score = random.random()
        if action_score < IGNORE_CHANCE:
            return self, other

        elif action_score - IGNORE_CHANCE < MATE_CHANCE and self._can_mate(other):
            return self._mate(other)

        else:
            return self._fight(other)

    def _can_mate(self, other: Organism) -> bool:
        return self.bio.gender != other.bio.gender and not any(agent.pregnant_with for agent in [self, other])

    def _fight(self, other: Organism) -> Tuple[BoardActor, BoardActor]:
        first, second = cast(Tuple[Organism, Organism], sorted([self, other], key=attrgettern('statistics', 'agility')))
        first_stats = first.statistics
        second_stats = second.statistics
        second_health_loss = max(first_stats.strength - second_stats.constitution, 1)

        if second_health_loss > second_stats.health:
            return first, SPACE

        first_health_loss = max(second_stats.strength - first_stats.constitution, 1)
        new_first_stats = first_stats.modify(health=lambda health: health - first_health_loss)
        new_second_stats = second_stats.modify(health=lambda health: health - second_health_loss)
        if first_health_loss > first_stats.health:
            return SPACE, second.modify(statistics=new_second_stats)

        return first.modify(statistics=new_first_stats), second.modify(statistics=new_second_stats)

    def _mate(self, other: Organism) -> Tuple[Organism, Organism]:
        child_genome = self.genome ^ other.genome
        # noinspection PyTypeChecker
        child_gender = Gender(random.randint(1, len(Gender)))

        if self.bio.gender is Gender.Female:
            child_bio = Bio(other, self, child_gender)
            return self.modify(pregnant_with=Egg.new(child_genome, child_bio)), other

        else:
            child_bio = Bio(self, other, child_gender)
            return self, other.modify(pregnant_with=Egg.new(child_genome, child_bio))


@dataclass(frozen=True)
class Bio:
    father: Organism
    mother: Organism
    gender: Gender


@dataclass(frozen=True)
class Statistics:
    strength: int
    agility: int
    constitution: int
    health: int

    def modify(self, strength: Statistic = None, agility: Statistic = None, constitution: Statistic = None,
               health: Statistic = None):
        # I wish I had type lambdas.
        return Statistics(orc(strength, self.strength), orc(agility, self.agility),
                          orc(constitution, self.constitution), orc(health, self.health))


class Effect(metaclass=ABCMeta):
    name: str

    @abstractmethod
    def modify(self, organism: Organism) -> Organism:
        pass

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Effect) and self.name == other.name


Effects = Set[Effect]
Statistic = Optional[Union[int, Callable[[int], int]]]
