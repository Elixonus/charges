from __future__ import annotations
from sys import getsizeof
from math import tau
from copy import copy
import csv
import numpy as np
from points import Point
from charges import System, PointCharge, ELEMENTARY_CHARGE
import sources as src

VIEWPORT_MINIMUM_X: float = 0.
VIEWPORT_MINIMUM_Y: float = 0.
VIEWPORT_MAXIMUM_X: float = 10.
VIEWPORT_MAXIMUM_Y: float = 10.
VIEWPORT_RANGE_X: float = VIEWPORT_MAXIMUM_X - VIEWPORT_MINIMUM_X
VIEWPORT_RANGE_Y: float = VIEWPORT_MAXIMUM_Y - VIEWPORT_MINIMUM_Y
IMAGE_LENGTH: int = 100
IMAGE_AREA: int = IMAGE_LENGTH ** 2

electric_system: System = System(PointCharge(-5 * ELEMENTARY_CHARGE, Point(5, 5)),
                                 PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
                                 PointCharge(-5 * ELEMENTARY_CHARGE, Point(2, 7)),
                                 PointCharge(-5 * ELEMENTARY_CHARGE, Point(2, 7)))

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

electric_potentials_sorted: list[float] = sorted(electric_potential
                                                 for electric_potentials_buffer in electric_potentials
                                                 for electric_potential in electric_potentials_buffer)
electric_potential_low: float = electric_potentials_sorted[round(0.01 * (IMAGE_AREA - 1))]
electric_potential_high: float = electric_potentials_sorted[round(0.99 * (IMAGE_AREA - 1))]
electric_equipotentials: list[float] = [
    electric_potentials_sorted[round(percentile * (IMAGE_AREA - 1))] for percentile in
    (0.05, 0.25, 0.5, 0.75, 0.95)
]


def viewport(point: Point, /) -> tuple[float, float]:
    return (point.x - VIEWPORT_MINIMUM_X) / VIEWPORT_RANGE_X,\
           (point.y - VIEWPORT_MINIMUM_Y) / VIEWPORT_RANGE_Y


points_x: list[float] = [VIEWPORT_MINIMUM_X + VIEWPORT_RANGE_X * index_x / (IMAGE_LENGTH - 1) for index_x in
                         range(IMAGE_LENGTH)]
points_y: list[float] = [VIEWPORT_MINIMUM_Y + VIEWPORT_RANGE_Y * index_y / (IMAGE_LENGTH - 1) for index_y in
                         range(IMAGE_LENGTH)]

electric_potentials: list[list[float]] = []

for point_x in points_x:
    electric_potentials_buffer: list[float] = []

    for point_y in points_y:
        electric_potential: float = electric_system.potential(Point(point_x, point_y))
        electric_potentials_buffer.append(electric_potential)

    electric_potentials.append(electric_potentials_buffer)

electric_potentials_flattened: list[float] = [electric_potential for electric_potentials_buffer in electric_potentials
                                              for electric_potential in electric_potentials_buffer]
electric_potentials_sorted: list[float] = sorted(electric_potentials_flattened)
electric_equipotential_low: float = electric_potentials_sorted[round(0.01 * (IMAGE_AREA - 1))]
electric_equipotential_high: float = electric_potentials_sorted[round(0.99 * (IMAGE_AREA - 1))]

electric_potentials_distorted: list[list[float]] = []

for electric_potentials_buffer in electric_potentials:
    electric_potentials_distorted_buffer: list[float] = []

    for electric_potential in electric_potentials_buffer:
        electric_potential_distorted: float = min(max((electric_potential - electric_equipotential_low) / (
                electric_equipotential_high - electric_equipotential_low), 0), 1)
        electric_potentials_distorted_buffer.append(electric_potential_distorted)

    electric_potentials_distorted.append(electric_potentials_distorted_buffer)

electric_equipotentials: list[float] = [electric_potentials_sorted[round(0.4 * (IMAGE_AREA - 1))]]

for electric_equipotential in electric_equipotentials:
    electric_potentials_flag: list[list[bool]] = [
        [electric_potential > electric_equipotential for electric_potential in electric_potentials_buffer] for
        electric_potentials_buffer in electric_potentials]

    electric_potentials_case: list[list[int]] = []

    for electric_potentials_flag_index, electric_potentials_flag_buffer in enumerate(electric_potentials_flag[:-1]):
        electric_potentials_case_buffer: list[int] = []

        for electric_potential_flag_index, electric_potential_flag in enumerate(electric_potentials_flag_buffer[:-1]):
            electric_potential_horizontal_flag: bool = electric_potentials_flag[electric_potentials_flag_index + 1][
                electric_potential_flag_index]
            electric_potential_vertical_flag: bool = electric_potentials_flag[electric_potentials_flag_index][
                electric_potential_flag_index + 1]
            electric_potential_diagonal_flag: bool = electric_potentials_flag[electric_potentials_flag_index + 1][
                electric_potential_flag_index + 1]
            electric_potential_case: int = 0

            if electric_potential_flag:
                electric_potential_case += 8

            if electric_potential_horizontal_flag:
                electric_potential_case += 4

            if electric_potential_diagonal_flag:
                electric_potential_case += 2

            if electric_potential_vertical_flag:
                electric_potential_case += 1

            electric_potentials_case_buffer.append(electric_potential_case)

        electric_potentials_case.append(electric_potentials_case_buffer)

with open("color_mapping.csv") as file:
    color_mapping: list[list[float]] = list(csv.reader(file, quoting=csv.QUOTE_NONNUMERIC))

image: list[list[list[float]]] = []

for electric_potentials_distorted_buffer in electric_potentials_distorted:
    image_buffer: list[list[float]] = []

    for electric_potential_distorted in electric_potentials_distorted_buffer:
        pixel: list[float] = [round(255 * channel) for channel in
                              color_mapping[round(255 * electric_potential_distorted)]]
        image_buffer.append(pixel)

    image.append(image_buffer)

# a = Image.fromarray(np.array(image).astype(np.uint8))
# a.show(a)
