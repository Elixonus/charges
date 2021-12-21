from __future__ import annotations
from sys import getsizeof
import csv
import numpy as np
import PIL.Image as Image
import electric_charges as ec

VIEWPORT_MINIMUM_X: float = 0.
VIEWPORT_MINIMUM_Y: float = 0.
VIEWPORT_MAXIMUM_X: float = 10.
VIEWPORT_MAXIMUM_Y: float = 10.
VIEWPORT_LENGTH: int = 500
VIEWPORT_AREA: int = VIEWPORT_LENGTH ** 2
ELECTRIC_FIELD_LINE_ITERATION_LIMIT: int = 500
ELECTRIC_FIELD_LINE_ITERATION_STEP: float = 0.1


class ElectricFieldLinesSourcePoints:
    point: int
    points: int
    endpoint_1: ec.Cartesian
    endpoint_2: ec.Cartesian

    def __init__(self, points: int, endpoint_1: ec.Cartesian, endpoint_2: ec.Cartesian):
        self.points = points
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2

    def __iter__(self):
        self.point = 0

    def __next__(self):
        point: ec.Cartesian = self.endpoint_2.copy().subtract(self.endpoint_1).multiply(self.point / (self.points - 1)).add(self.endpoint_1)
        self.point += 1
        return point

system: ec.System = ec.System(ec.PointCharge(5 * ec.ELEMENTARY_CHARGE, ec.Cartesian(5, 5)),
                              ec.PointCharge(-5 * ec.ELEMENTARY_CHARGE, ec.Cartesian(7, 5)),
                              ec.PointCharge(-5 * ec.ELEMENTARY_CHARGE, ec.Cartesian(2, 7)),
                              ec.PointCharge(-5 * ec.ELEMENTARY_CHARGE, ec.Cartesian(2, 7)))


sources_electric_field_lines: list[tuple[ec.Cartesian, ec.Cartesian, int]] = [(ec.Cartesian(0, 0), ec.Cartesian(1, 1), 5)]

electric_field_line_start_position: ec.Cartesian = ec.Cartesian(0, 0)

# Contains electric field line points from positive to negative direction
electric_field_line_points: list[ec.Cartesian] = []

electric_field: ec.Cartesian
electric_field_unit: ec.Cartesian

# Finding and recording electric field line points from source to positive
electric_field_line_point: ec.Cartesian = electric_field_line_start_position.copy()
for electric_field_line_iteration in range(ELECTRIC_FIELD_LINE_ITERATION_LIMIT):
    electric_field = system.electric_field(electric_field_line_point)
    electric_field_unit = electric_field.normalize()
    electric_field_line_point.subtract(electric_field_unit)
    electric_field_line_points.append(electric_field_line_point.copy())

# Recording electric field line point at source
electric_field_line_points.reverse()
electric_field_line_points.append(electric_field_line_start_position)

# Finding and recording electric field line points from source to negative
electric_field_line_point.change(electric_field_line_start_position.copy())
for electric_field_line_iteration in range(ELECTRIC_FIELD_LINE_ITERATION_LIMIT):
    electric_field = system.electric_field(electric_field_line_point)
    electric_field_unit = electric_field.normalize()
    electric_field_line_point.add(electric_field_unit)
    electric_field_line_points.append(electric_field_line_point.copy())


# for electric_field_line_iteration in range(ELECTRIC_FIELD_LINE_ITERATION_LIMIT):





points_x: list[float] = [VIEWPORT_MINIMUM_X + (VIEWPORT_MAXIMUM_X - VIEWPORT_MINIMUM_X) * index_x / (VIEWPORT_LENGTH - 1) for index_x in range(VIEWPORT_LENGTH)]
points_y: list[float] = [VIEWPORT_MINIMUM_Y + (VIEWPORT_MAXIMUM_Y - VIEWPORT_MINIMUM_Y) * index_y / (VIEWPORT_LENGTH - 1) for index_y in range(VIEWPORT_LENGTH)]

electric_potentials: list[list[float]] = []

for point_x in points_x:
    electric_potentials_buffer: list[float] = []

    for point_y in points_y:
        electric_potential: float = system.electric_potential(ec.Cartesian(point_x, point_y))
        electric_potentials_buffer.append(electric_potential)

    electric_potentials.append(electric_potentials_buffer)

electric_potentials_flattened: list[float] = [electric_potential for electric_potentials_buffer in electric_potentials for electric_potential in electric_potentials_buffer]
electric_potentials_sorted: list[float] = sorted(electric_potentials_flattened)
electric_potential_low: float = electric_potentials_sorted[round(0.01 * (VIEWPORT_AREA - 1))]
electric_potential_high: float = electric_potentials_sorted[round(0.99 * (VIEWPORT_AREA - 1))]

electric_potentials_normalized: list[list[float]] = []

for electric_potentials_buffer in electric_potentials:
    electric_potentials_normalized_buffer: list[float] = []

    for electric_potential in electric_potentials_buffer:
        electric_potential_normalized: float = min(max((electric_potential - electric_potential_low) / (electric_potential_high - electric_potential_low), 0), 1)
        electric_potentials_normalized_buffer.append(electric_potential_normalized)

    electric_potentials_normalized.append(electric_potentials_normalized_buffer)

electric_equipotentials: list[float] = [electric_potentials_sorted[round(0.4 * (VIEWPORT_AREA - 1))]]

for electric_equipotential in electric_equipotentials:
    electric_potentials_flag: list[list[bool]] = [[electric_potential > electric_equipotential for electric_potential in electric_potentials_buffer] for electric_potentials_buffer in electric_potentials]

    electric_potentials_case: list[list[int]] = []

    for electric_potentials_flag_index, electric_potentials_flag_buffer in enumerate(electric_potentials_flag[:-1]):
        electric_potentials_case_buffer: list[int] = []

        for electric_potential_flag_index, electric_potential_flag in enumerate(electric_potentials_flag_buffer[:-1]):
            electric_potential_horizontal_flag: bool = electric_potentials_flag[electric_potentials_flag_index + 1][electric_potential_flag_index]
            electric_potential_vertical_flag: bool = electric_potentials_flag[electric_potentials_flag_index][electric_potential_flag_index + 1]
            electric_potential_diagonal_flag: bool = electric_potentials_flag[electric_potentials_flag_index + 1][electric_potential_flag_index + 1]
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

for electric_potentials_normalized_buffer in electric_potentials_normalized:
    image_buffer: list[list[float]] = []

    for electric_potential_normalized in electric_potentials_normalized_buffer:
        pixel: list[float] = [round(255 * channel) for channel in color_mapping[round(255 * electric_potential_normalized)]]
        image_buffer.append(pixel)

    image.append(image_buffer)

a = Image.fromarray(np.array(image).astype(np.uint8))
a.show(a)


'''plt.figure()
plt.colorbar(plt.contourf(points_x, points_y, electric_potentials, levels=critical_electric_potentials, extend="both"), drawedges=True)
plt.contour(points_x, points_y, electric_potentials, levels=critical_electric_potentials, colors="black")
plt.show()
'''