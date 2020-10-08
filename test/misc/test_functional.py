import pytest

from pydenim.misc.functional import orc


@pytest.mark.parametrize(['left', 'right', 'expected'], [
    (1, 0, 1),
    (0, 2, 2),
    (None, 2, 2),
    (1, 2, 1),
    (1, lambda x: x + 1, 2)
])
def test_orc(left, right, expected):
    assert orc(left, right) == expected
