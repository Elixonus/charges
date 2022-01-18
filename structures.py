from __future__ import annotations
from math import tau
from points import Point
from charges import Charge, System, PointCharge


class Structure(System):
    def __init__(self, charges: list[Charge]):
        super().__init__(charges)


class CircleStructure(Structure):
    def __init__(self, center: Point, radius: float, charge: float, elements: int) -> None:
        charges = [
            PointCharge(charge / elements, center + Point.polar(radius, tau * (element / elements)))
            for element in range(elements)
        ]
        super().__init__(charges)



class PolygonStructure(Structure):
    charges: list[Charge]

    def __init__(self):
