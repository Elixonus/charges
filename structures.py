from __future__ import annotations
from math import tau
from points import Point
from charges import Charge, PointCharge


class Structure(Charge):
    members: list[PointCharge]
    position: Point

    def __init__(self, members: list[PointCharge], position: Point):
        super().__init__()
        self.members = members
        self.position = position

    def field(self, point: Point) -> Point:
        field = Point(0, 0)
        for charge in self.members:
            field += charge.field(point - self.position)
        return field

    def potential(self, point: Point) -> float:
        potential = 0
        for charge in self.members:
            potential += charge.potential(point - self.position)
        return potential

class FiniteLineStructure(Structure):
    def __init__(self, charge: float, position, length, elements: int) -> None:
        members = [
            PointCharge(
                charge / elements,
                Point((element / (elements - 1) - 0.5) * length, 0)
            )
            for element in range(elements)
        ]
        super().__init__(members, position)

class CircleStructure(Structure):
    def __init__(self, charge: float, position: Point, radius: float, elements: int) -> None:
        members = [
            PointCharge(
                charge / elements,
                Point.polar(radius, tau * (element / elements))
            )
            for element in range(elements)
        ]
        super().__init__(members, position)

c = CircleStructure(5, Point(1, 1), 5, 10)