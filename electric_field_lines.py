from __future__ import annotations
from math import tau
from typing import Iterator
import points as pt


class LineSource:
    sources: int
    endpoint_1: pt.Cartesian
    endpoint_2: pt.Cartesian

    def __init__(self, sources: int, endpoint_1: pt.Cartesian, endpoint_2: pt.Cartesian) -> None:
        self.sources = sources
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2

    def points(self) -> Iterator[pt.Cartesian]:
        for source in range(self.sources):
            point: pt.Cartesian = self.endpoint_2.copy().subtract(self.endpoint_1).multiply(source / (self.sources - 1)).add(self.endpoint_1)
            yield point


class CircleSource:
    sources: int
    center: pt.Cartesian
    radius: float

    def __init__(self, sources: int, center: pt.Cartesian, radius: float):
        self.sources = sources
        self.center = center
        self.radius = radius

    def points(self) -> Iterator[pt.Cartesian]:
        for source in range(self.sources):
            point: pt.Cartesian = pt.Polar(self.radius, tau * source / self.sources).cartesian()
            yield point
