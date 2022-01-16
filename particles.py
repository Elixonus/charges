from __future__ import annotations
from points import Point
from charges import PointCharge


class System:
    particles: list[Particle]

    def __init__(self, particles: list[Particle]):
        self.particles = particles


class Particle(PointCharge):
    mass: float
    velocity: Point
    acceleration: Point

    def __init__(self, mass: float, charge: float, point: Point, velocity: Point, acceleration: Point) -> None:
        super().__init__(charge, point)
        self.mass = mass
        self.velocity = velocity
        self.acceleration = acceleration

    def force(self, particle: Particle) -> Point:
        force = self.field(particle.point).mul(particle.charge)
        return force