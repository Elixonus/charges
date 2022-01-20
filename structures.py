from __future__ import annotations
from math import tau
from itertools import pairwise
from points import Point
from charges import Charge, PointCharge


class Structure(Charge):
    members: list[Charge]
    position: Point

    def __init__(self, members: list[Charge], position: Point):
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
    def __init__(self, charge: float, position: Point, length: float, members: int) -> None:
        point_charges = []
        for member in range(members):
            point_charge = PointCharge(charge / members, Point((member / (members - 1) - 0.5) * length, 0))
            point_charges.append(point_charge)
        super().__init__(point_charges, position)


class CircleStructure(Structure):
    def __init__(self, charge: float, position: Point, radius: float, members: int) -> None:
        point_charges = []
        for member in range(members):
            point_charge = PointCharge(charge / members, Point.polar(radius, tau * (member / members)))
            point_charges.append(point_charge)
        super().__init__(point_charges, position)


class PathStructure(Structure):
    def __init__(self, charge: float, position: Point, vertices: list[Point], members: int) -> None:
        point_charges = []
        perimeter: float = sum(vertex_1.dist(vertex_2) for vertex_1, vertex_2 in pairwise(vertices))

c = CircleStructure(5, Point(1, 1), 5, 10)