from __future__ import annotations
from math import tau
from points import Point
from charges import Charge, PointCharge


class Structure(Charge):
    charges: list[PointCharge]
    position: Point

    def __init__(self, charges: list[PointCharge], position: Point):
        super().__init__()
        self.charges = charges
        self.position = position

    def field(self, point: Point) -> Point:
        field = Point(0, 0)
        for charge in self.charges:
            field += charge.field(point - self.position)
        return field

    def potential(self, point: Point) -> float:
        potential = 0
        for charge in self.charges:
            potential += charge.potential(point - self.position)
        return potential


class CircleStructure(Structure):
    def __init__(self, charge: float, position: Point, radius: float, members: int) -> None:
        charges = [
            PointCharge(
                charge / members,
                Point.polar(radius, tau * (member / members))
            )
            for member in range(members)
        ]
        super().__init__(charges, position)


c = CircleStructure(5, Point(1, 1), 5, 10)