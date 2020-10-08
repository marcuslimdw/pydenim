from pydenim.genetics.gene import Genome, Gene, Modifier
from pydenim.misc.internal_types import Statistic
from pydenim.objects.organism import Statistics


def test_genome():
    genome = Genome([
        Gene([
            Modifier(Statistic.Strength, 3),
            Modifier(Statistic.Agility, 2)
        ]),
        Gene([
            Modifier(Statistic.Agility, -1),
            Modifier(Statistic.Constitution, 2)
        ])
    ])
    assert genome.generate_statistics() == Statistics(strength=3, agility=1, constitution=2, health=100)
