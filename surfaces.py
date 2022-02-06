from math import tau
from typing import Iterator
from points import Point
from charges import System, Charge, PointCharge


def line_charge(charge: float, point_1: Point, point_2: Point, point_charges: int) -> Iterator[PointCharge]:
    for point_charge in range(point_charges):
        yield PointCharge(
            charge=charge / point_charges,
            point=point_1 + (point_2 - point_1) * point_charge / (point_charges - 1)
        )


def circle_charge(charge: float, point: Point, radius: float, point_charges: int) -> Iterator[PointCharge]:
    for point_charge in range(point_charges):
        yield PointCharge(
            charge=charge / point_charges,
            point=Point.polar(radius, tau * point_charge / point_charges)
        )


def interpolate(point_1: Point, point_2: Point, interpolation: float) -> Point:
    return point_1 + (point_2 - point_1) * interpolation


mycharge = LineCharge(5, Point(4, 3), Point(0, 0), 20)
print(mycharge.charge)