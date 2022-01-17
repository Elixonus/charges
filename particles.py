from __future__ import annotations
from itertools import combinations
from points import Point
from charges import PointCharge


class System:
    particles: list[Particle]

    def __init__(self, particles: list[Particle]):
        self.particles = particles

    def simulate(self, step):
        for particle_1, particle_2 in combinations(self.particles, 2):
            force_1 = particle_1.force(particle_2)
            force_2 = -force_1
            acceleration_1 = force_1 / particle_1.mass
            acceleration_2 = force_2 / particle_2.mass
            particle_1.velocity.add(step * acceleration_1)
            particle_2.velocity.add(step * acceleration_2)


class Particle(PointCharge):
    mass: float
    velocity: Point

    def __init__(self, *, mass: float, charge: float, point: Point, velocity: Point) -> None:
        super().__init__(charge, point)
        self.mass = mass
        self.velocity = velocity

    def force(self, particle: Particle) -> Point:
        force = self.field(particle.point).mul(particle.charge)
        return force


pp = Particle(mass=5, charge=2, point=Point(4, 3), velocity=Point(0, 0))
pp.position = Point(5, 5)
print(pp.point.x)