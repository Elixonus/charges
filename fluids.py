from __future__ import annotations
from points import Point
from charges import PointCharge


class Particle(PointCharge):
    mass: float
    position: Point
    velocity: Point

    def __init__(self, mass: float, charge: float, position: Point, velocity: Point) -> None:
        super().__init__(charge, position)
        self.mass = mass
        self.position = position
        self.velocity = velocity