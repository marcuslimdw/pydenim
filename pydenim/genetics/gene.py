from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import chain, groupby
from typing import List, NamedTuple

from pydenim.misc.constants import MUTATION_CHANCE
from pydenim.misc.functional import either, attrgettern
from pydenim.misc.internal_types import Statistic
from pydenim.objects.organism import Statistics


class Modifier(NamedTuple):
    statistic: Statistic
    amount: float


@dataclass(frozen=True)
class Gene:
    modifiers: List[Modifier]

    def mutate(self) -> Gene:
        if random.random() >= MUTATION_CHANCE:
            return self

        return self


@dataclass(frozen=True)
class Genome:
    genes: List[Gene]

    def __xor__(self, other: Genome) -> Genome:
        genes = [either(left_gene, right_gene).mutate() for left_gene, right_gene in zip(self.genes, other.genes)]
        return Genome(genes)

    def generate_statistics(self) -> Statistics:
        all_modifiers = chain.from_iterable(gene.modifiers for gene in self.genes)
        by_statistic = attrgettern('statistic', 'name')
        grouped = groupby(sorted(all_modifiers, key=by_statistic), by_statistic)
        statistics = {stat.lower(): sum(modifier for _, modifier in group) for stat, group in grouped}
        return Statistics(health=100, **statistics)
