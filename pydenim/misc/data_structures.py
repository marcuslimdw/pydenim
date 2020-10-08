from __future__ import annotations

import copy
from typing import List, Tuple, Union, Callable, TypeVar, Generic, Iterable, NamedTuple, Optional

T = TypeVar('T')
U = TypeVar('U')

SetterValue = Union[T, Iterable[T], Iterable[Iterable[T]]]
Dims = Tuple[int, int]
Coordinate = Union[int, slice]
Coordinates = Tuple[Coordinate, Coordinate]


# My side projects have side projects...


class Bounds(NamedTuple):
    x_min: int
    x_max: int
    y_min: int
    y_max: int


# TODO: Make this a SliceableNDList :)


class Sliceable2DList(Generic[T]):

    def __init__(self, data: Iterable[Iterable[T]]):
        self._data, (n_rows, n_cols) = self._validate_dims(data)
        self._parent = None
        self._bounds = Bounds(0, n_cols, 0, n_rows)
        self.dims = (n_rows, n_cols)

    def __iter__(self):
        return iter(self._data)

    def __eq__(self, other):
        return self.values == other

    def __getitem__(self, coordinates: Coordinates) -> Union[T, Sliceable2DList[T]]:
        proper_x, proper_y = self._adjust(coordinates)
        if isinstance(proper_y, slice):
            if isinstance(proper_x, slice):
                return self._from_parent(self._slices_to_bounds(proper_x, proper_y))

            else:
                return [row[proper_x] for row in self._data[proper_y]]

        else:
            return self._data[proper_y][proper_x]

    def __setitem__(self, coordinates: Coordinates, value: SetterValue):
        proper_x, proper_y = self._adjust(coordinates)
        if isinstance(proper_x, int) and isinstance(proper_y, int):
            self._data[proper_y][proper_x] = value

        elif isinstance(proper_x, int):
            y_extent = proper_y.stop - proper_y.start
            elements = list(value)
            if (size := len(elements)) != proper_y.stop - proper_y.start:
                raise ValueError(f'Could not fill a column of size {y_extent} with data of size {size}.')

            for y, element in enumerate(elements, proper_y.start):
                self._data[y][proper_x] = element

        elif isinstance(proper_y, int):
            x_extent = proper_x.stop - proper_x.start
            elements = list(value)
            if (size := len(elements)) != proper_x.stop - proper_x.start:
                raise ValueError(f'Could not fill a column of size {x_extent} with data of size {size}.')

            self._data[proper_y][proper_x] = elements

        else:
            x_extent = proper_x.stop - proper_x.start
            y_extent = proper_y.stop - proper_y.start
            elements, dims = self._validate_dims(value)
            n_rows, n_cols = dims
            if (x_extent != n_cols) or (y_extent != n_rows):
                raise ValueError(f'Could not fill a block of shape {(x_extent, y_extent)} with data of shape {dims}.')

            for y, row in enumerate(elements, proper_y.start):
                self._data[y][proper_x] = row

    @property
    def values(self):
        x_min, x_max, y_min, y_max = self._bounds
        return [row[x_min:x_max] for row in self._data[y_min:y_max]]

    @property
    def inner(self) -> Sliceable2DList[T]:
        x_min, x_max, y_min, y_max = self._bounds
        new_bounds = Bounds(x_min + 1, x_max - 1, y_min + 1, y_max - 1)
        return self._from_parent(new_bounds)

    @inner.setter
    def inner(self, value: SetterValue):
        self.inner[:, :] = value

    def apply(self, f: Callable[[T], U]):
        data = self._data
        x_min, x_max, y_min, y_max = self._bounds
        for y in range(y_min, y_max):
            row = data[y]
            for x in range(x_min, x_max):
                row[x] = f(row[x])

    def iter_coords(self):
        data = self._data
        x_min, x_max, y_min, y_max = self._bounds
        for y in range(y_min, y_max):
            row = data[y]
            for x in range(x_min, x_max):
                yield x, y, row[x]

    def fill(self, fill_value: T):
        self.apply(lambda element: fill_value)

    def replace(self, to_replace: T, replace_with: T):
        self.apply(lambda element: replace_with if element == to_replace else element)

    def map(self, f: Callable[[T], U]) -> Sliceable2DList[U]:
        x_min, x_max, y_min, y_max = self._bounds
        return Sliceable2DList([[f(element) for element in row[x_min:x_max]] for row in self._data[y_min:y_max]])

    @classmethod
    def uniform(cls, n_rows: int, n_cols: int, fill_value: Optional[T] = None) -> Sliceable2DList[T]:
        return Sliceable2DList([[fill_value for _ in range(n_cols)] for _ in range(n_rows)])

    def _adjust(self, coordinates: Coordinates):
        def adjust_individual(coordinate: Coordinate, min_bound: int, max_bound: int):
            if isinstance(coordinate, int):
                return min_bound + coordinate if coordinate >= 0 else max_bound + coordinate

            elif isinstance(coordinate, slice):
                if (start := coordinate.start) is None:
                    proper_start = min_bound

                else:
                    proper_start = start + (min_bound if start >= 0 else max_bound)

                if (stop := coordinate.stop) is None:
                    proper_stop = max_bound

                else:
                    proper_stop = stop + (min_bound if stop >= 0 else max_bound)

                return slice(proper_start, proper_stop)

            else:
                raise TypeError(coordinate)

        x, y = coordinates
        x_min, x_max, y_min, y_max = self._bounds
        return adjust_individual(x, x_min, x_max), adjust_individual(y, y_min, y_max)

    def _from_parent(self, bounds: Bounds) -> Sliceable2DList[T]:
        child = copy.copy(self)
        child._parent = self
        child._bounds = self._clip_bounds(bounds, self.dims)
        return child

    def _slices_to_bounds(self, x_slice: slice, y_slice: slice) -> Bounds:
        n_rows, n_cols = self.dims
        x_max = n_cols - 1 if x_slice.stop is None else x_slice.stop
        y_max = n_rows - 1 if y_slice.stop is None else y_slice.stop
        return Bounds(x_slice.start or 0, x_max, y_slice.start or 0, y_max)

    @staticmethod
    def _validate_dims(data: Iterable[Iterable[T]]) -> Tuple[List[List[T]], Dims]:
        list_data = [list(row) for row in data]
        n_rows = len(list_data)
        col_counts = {len(row) for row in list_data}
        if not col_counts:
            return list_data, (n_rows, 0)

        elif len(col_counts) == 1:
            return list_data, (n_rows, col_counts.pop())

        else:
            raise TypeError('Got unevenly shaped data.')

    @staticmethod
    def _clip_bounds(bounds: Bounds, dims: Dims):
        def clip(lower: int, upper: int, dim: int) -> Dims:
            real_lower = max(lower if lower >= 0 else dim + lower, 0)
            real_upper = min(upper if upper >= 0 else dim + upper, dim)
            return (real_lower, real_upper) if real_lower <= real_upper else (real_upper, real_upper)

        x_min, x_max, y_min, y_max = bounds
        n_rows, n_cols = dims
        return Bounds(*clip(x_min, x_max, n_cols), *clip(y_min, y_max, n_rows))

    def __str__(self):
        def enclose(string):
            return f'[{string}]'

        return enclose('\n '.join(enclose(', '.join(element for element in row)) for row in self.map(str)._data))

    def __repr__(self):
        return self.__str__()
