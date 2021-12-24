from __future__ import annotations
from math import tau
from copy import copy
from collections.abc import Iterator
from typing import TypeAlias
import points as pt


class LineSource:
    sources: int
    endpoint_1: pt.Point
    endpoint_2: pt.Point

    def __init__(self, sources: int, endpoint_1: pt.Point, endpoint_2: pt.Point) -> None:
        self.sources = sources
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2

    def points(self) -> Iterator[pt.Point]:
        for source in range(self.sources):
            point: pt.Point = copy(self.endpoint_2).subtract(self.endpoint_1).multiply(source / (self.sources - 1)).add(self.endpoint_1)
            yield point


class CircleSource:
    sources: int
    point: pt.Point
    radius: float

    def __init__(self, sources: int, point: pt.Point, radius: float):
        self.sources = sources
        self.point = point
        self.radius = radius

    def points(self) -> Iterator[pt.Point]:
        for source in range(self.sources):
            point: pt.Point = pt.Point.polar(self.radius, tau * source / self.sources)
            yield point


Source: TypeAlias = LineSource | CircleSource
