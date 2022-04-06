from __future__ import annotations
from points import Point
from charges import Charge, PointCharge


class Structure(Charge):
    members: list[Charge]

    def __init__(self, members: list[Charge]) -> None:
        super().__init__()
        self.members = members

    def field(self, point: Point) -> Point:
        field = Point(0, 0, 0)
        for charge in self.members:
            field += charge.field(point)
        return field

    def potential(self, point: Point) -> float:
        potential = 0
        for charge in self.members:
            potential += charge.potential(point)
        return potential


class FiniteLineStructure(Structure):
    def __init__(self, charge: float, position_1: Point, position_2: Point, members: int) -> None:
        charges = [PointCharge(charge / members, position_1 + (position_2 - position_1) * member / (members - 1))
                   for member in range(members)]
        super().__init__(charges)
