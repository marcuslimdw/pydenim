from enum import Enum


class Statistic(Enum):
    Strength = 1
    Agility = 2
    Constitution = 3


# Something I have always found rather strange: why does "male" tend to come before "female" in gender choices, since
# the only reasonable ordering I can think of is alphabetical?

class Gender(Enum):
    Female = 1
    Male = 2
