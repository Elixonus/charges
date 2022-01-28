from __future__ import annotations
import cairo
from particles import System, Particle, Point

system = System([Particle(charge=1e-7, mass=1, position=Point(0.4, 0.2), velocity=Point(0.04, 0.04)),
                 Particle(charge=1e-7, mass=1, position=Point(0.4, 0.4), velocity=Point(0, 0)),
                 Particle(charge=1e-7, mass=1, position=Point(0.6, 0.4), velocity=Point(0.02, 0))])

with cairo.ImageSurface(cairo.Format.RGB24, 300, 300) as surface:
    context = cairo.Context(surface)
    context.scale(300, 300)

    for i in range(100):
        for particle in system.particles:
            context.rectangle(particle.point.x, particle.point.y, 0.002, 0.002)
            context.set_source_rgb(1, 0, 0)
            context.fill()

        system.iterate(1)

    surface.write_to_png("cairo.png")