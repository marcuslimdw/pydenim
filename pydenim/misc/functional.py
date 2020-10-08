import random
from functools import reduce
from typing import TypeVar, Sequence, Callable, Union, Iterable

T = TypeVar('T')


def choice(seq: Sequence[T]) -> T:
    return random.choice(seq)


def either(left: T, right: T) -> T:
    return left if random.random() < 0.5 else right


def randint(low: int, high: int) -> int:
    return random.randint(low, high)


def orc(left: T, right: Union[T, Callable[[T], T]]) -> T:
    return right(left) if callable(right) else left or right


def attrgettern(*attrs: Iterable[str]) -> Callable:
    def wrapped(value):
        return reduce(lambda intermediate, attr: getattr(intermediate, attr), attrs, value)

    return wrapped
