from __future__ import annotations
from sys import getsizeof
from math import tau
from copy import copy
import csv
import numpy as np
import cairo
from points import Point
from charges import System, PointCharge, ELEMENTARY_CHARGE
import sources as src

VIEWPORT_MINIMUM_X: float = 0.
VIEWPORT_MINIMUM_Y: float = 0.
VIEWPORT_MAXIMUM_X: float = 10.
VIEWPORT_MAXIMUM_Y: float = 10.
VIEWPORT_RANGE_X: float = VIEWPORT_MAXIMUM_X - VIEWPORT_MINIMUM_X
VIEWPORT_RANGE_Y: float = VIEWPORT_MAXIMUM_Y - VIEWPORT_MINIMUM_Y
IMAGE_LENGTH: int = 400
IMAGE_AREA: int = IMAGE_LENGTH ** 2

electric_system: System = System(
    PointCharge(5 * ELEMENTARY_CHARGE, Point(5, 5)),
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
    PointCharge(5 * ELEMENTARY_CHARGE, Point(5, 7)))

ELECTRIC_FIELD_LINE_ITERATION_LIMIT: int = 1000
ELECTRIC_FIELD_LINE_ITERATION_STEP: float = 0.01

electric_field_lines_source_points: list[Point] = [Point(4, 3), Point(5, 0.99), Point(5, 3), Point(2, 2)]
electric_field_lines_points: list[list[Point]] = []

for electric_field_line_source_point in electric_field_lines_source_points:
    # Contains electric field line points from positive to negative direction
    electric_field_line_points: list[Point] = []
    electric_field_line_point: Point
    electric_field: Point

    # Finding and recording electric field line points from source to positive
    electric_field_line_point = copy(electric_field_line_source_point)
    for electric_field_line_iteration in range(ELECTRIC_FIELD_LINE_ITERATION_LIMIT):
        electric_field = electric_system.field(electric_field_line_point)
        electric_field_line_point.subtract(
            electric_field.divide(electric_field.length()).multiply(ELECTRIC_FIELD_LINE_ITERATION_STEP))
        electric_field_line_points.append(copy(electric_field_line_point))

    # Recording electric field line point at source
    electric_field_line_points.reverse()
    electric_field_line_points.append(copy(electric_field_line_source_point))

    # Finding and recording electric field line points from source to negative
    electric_field_line_point = copy(electric_field_line_source_point)
    for electric_field_line_iteration in range(ELECTRIC_FIELD_LINE_ITERATION_LIMIT):
        electric_field = electric_system.field(electric_field_line_point)
        electric_field_line_point.add(
            electric_field.divide(electric_field.length()).multiply(ELECTRIC_FIELD_LINE_ITERATION_STEP))
        electric_field_line_points.append(copy(electric_field_line_point))

    electric_field_lines_points.append(electric_field_line_points)

electric_fields: list[list[Point]] = [[electric_system.field(Point(
    VIEWPORT_MINIMUM_X + VIEWPORT_RANGE_X * (image_x / (IMAGE_LENGTH - 1)),
    VIEWPORT_MINIMUM_Y + VIEWPORT_RANGE_Y * (image_y / (IMAGE_LENGTH - 1))
)) for image_y in range(IMAGE_LENGTH)] for image_x in range(IMAGE_LENGTH)]

electric_potentials: list[list[float]] = [[electric_system.potential(Point(
    VIEWPORT_MINIMUM_X + VIEWPORT_RANGE_X * (image_x / (IMAGE_LENGTH - 1)),
    VIEWPORT_MINIMUM_Y + VIEWPORT_RANGE_Y * (image_y / (IMAGE_LENGTH - 1))
)) for image_y in range(IMAGE_LENGTH)] for image_x in range(IMAGE_LENGTH)]

electric_potentials_sorted: list[float] = sorted(
    electric_potential
    for electric_potentials_buffer in electric_potentials
    for electric_potential in electric_potentials_buffer)
electric_potential_low: float = electric_potentials_sorted[round(0.005 * (IMAGE_AREA - 1))]
electric_potential_high: float = electric_potentials_sorted[round(0.995 * (IMAGE_AREA - 1))]
electric_equipotentials: list[float] = [
    electric_potentials_sorted[round(percentile * (IMAGE_AREA - 1))] for percentile in
    (0.05, 0.25, 0.5, 0.75, 0.95)
]

with open("colors.txt") as file:
    colors: list[list[float]] = [[float(value) for value in line.split(sep=" ")] for line in
                                 file.read().split(sep="\n")]

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, IMAGE_LENGTH, IMAGE_LENGTH)
ctx = cairo.Context(surface)

for x in range(IMAGE_LENGTH):
    for y in range(IMAGE_LENGTH):
        ctx.rectangle(x, y, 1, 1)
        normalized_electric_potential = min(max((electric_potentials[x][y] - electric_potential_low) /
                                                (electric_potential_high - electric_potential_low), 0), 1)
        ctx.set_source_rgb(*colors[round(255 * normalized_electric_potential)])
        ctx.fill()

surface.write_to_png("drawing.png")


def viewport(point: Point, /) -> tuple[float, float]:
    return (point.x - VIEWPORT_MINIMUM_X) / VIEWPORT_RANGE_X, \
           (point.y - VIEWPORT_MINIMUM_Y) / VIEWPORT_RANGE_Y
