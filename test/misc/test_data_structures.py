import pytest

from pydenim.misc.data_structures import Sliceable2DList


@pytest.mark.parametrize(['data', 'coordinates', 'value', 'expected'], [
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (0, 0),
        0,
        [
            [0, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (-1, -1),
        0,
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (slice(0, -1), 0),
        [0, 0],
        [
            [0, 0, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (slice(0, None), 0),
        [0, 0, 0],
        [
            [0, 0, 0],
            [4, 5, 6],
            [7, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (0, slice(0, -1)),
        [0, 0],
        [
            [0, 2, 3],
            [0, 5, 6],
            [7, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (0, slice(0, None)),
        [0, 0, 0],
        [
            [0, 2, 3],
            [0, 5, 6],
            [0, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (slice(0, -1), slice(0, -1)),
        [[0, 0],
         [0, 0]],
        [
            [0, 0, 3],
            [0, 0, 6],
            [7, 8, 9]
        ]
    ),
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (slice(1, None), slice(1, None)),
        [
            [0, 0],
            [0, 0]
        ],
        [
            [1, 2, 3],
            [4, 0, 0],
            [7, 0, 0]
        ]
    ),
])
def test_setitem(data, coordinates, value, expected):
    list_data = Sliceable2DList(data)
    list_data[coordinates] = value
    assert list_data == expected


@pytest.mark.parametrize(['data', 'coordinates', 'value'], [
    pytest.param(
        [
            [1, 2],
            [3, 4]
        ],
        (0, 0),
        1
    ),
    pytest.param(
        [
            [1, 2],
            [3, 4]
        ],
        (slice(0, None), 0),
        [1, 2]
    ),
    pytest.param(
        [
            [1, 2],
            [3, 4]
        ],
        (0, slice(0, None)),
        [1, 3]
    ),
])
def test_getitem(data, coordinates, value):
    assert Sliceable2DList(data)[coordinates] == value


@pytest.mark.parametrize(['data', 'coordinates', 'value'], [
    pytest.param(
        [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        (slice(0, -1), slice(0, -1)),
        [
            [1, 2],
            [4, 5]
        ]
    )
])
def test_eq(data, coordinates, value):
    assert Sliceable2DList(data)[coordinates] == value
