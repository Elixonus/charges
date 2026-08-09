from __future__ import annotations
from itertools import combinations
from charges import PointCharge, Point


class System:
    """System of charged particles."""

    particles: list[Particle]

    def __init__(self, particles: list[Particle]) -> None:
        """Create a system of charged particles."""
        self.particles = particles

    def momentum(self) -> Point:
        momentum = Point(0, 0)
        for particle in self.particles:
            momentum += particle.momentum()
        return momentum

    def iterate(self, time: float) -> System:
        # Calculation of velocity.
        for particle_1, particle_2 in combinations(self.particles, 2):
            particle_1.velocity += (
                particle_1.force(particle_2) / particle_1.mass
            ) * time
            particle_2.velocity += (
                particle_2.force(particle_1) / particle_2.mass
            ) * time
        # Calculation of position.
        for particle in self.particles:
            particle.iterate(time)
        return self


class Particle(PointCharge):
    """Charged particle with mass and velocity."""

    mass: float
    velocity: Point

    def __init__(
        self, charge: float, mass: float, position: Point, velocity: Point
    ) -> None:
        """Create a charged particle."""
        super().__init__(charge, position)
        self.mass = mass
        self.velocity = velocity

    def momentum(self) -> Point:
        return self.mass * self.velocity

    def iterate(self, time: float) -> Particle:
        self.point += self.velocity * time
        return self

    def force(self, particle: Particle) -> Point:
        """Calculate the electric force applied on the particle itself."""
        force = self.field(particle.point) * particle.charge
        return force


try:
    if __name__ == "__main__":
        from time import sleep

        print(
            "This python file is just a library, feel free to try out the other programs."
        )
        sleep(5)
except KeyboardInterrupt:
    exit()
