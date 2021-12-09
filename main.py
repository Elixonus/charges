from __future__ import annotations
from math import atan2, cos, hypot, inf, pi, sin, sqrt, tau
import numpy as np
import matplotlib.pyplot as plt

ELECTROSTATIC_CONSTANT: float = 8.9875517923E+9
ELEMENTARY_CHARGE: float = 1.602176634E-19

class System:
    charges: list[PointCharge]

    def __init__(self, charges: list[PointCharge]) -> None:
        self.charges = charges

    def electric_field(self, point: Cartesian) -> Cartesian:
        electric_field: Cartesian = Cartesian(0, 0)
        for charge in self.charges:
            electric_field.add(charge.electric_field(point))
        return electric_field

    def electric_potential(self, point: Cartesian) -> float:
        electric_potential: float = 0.
        for charge in self.charges:
            electric_potential += charge.electric_potential(point)
        return electric_potential


class PointCharge:
    charge: float
    position: Cartesian

    def __init__(self, charge: float, position: Cartesian) -> None:
        self.charge = charge
        self.position = position

    def electric_field(self, point: Cartesian) -> Cartesian:
        electric_field: Cartesian
        try:
            electric_field = Polar(ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point) ** 2,
                                   self.position.angle(point)).cartesian()
        except ZeroDivisionError:
            electric_field = Cartesian(0, 0)
        return electric_field

    def electric_potential(self, point: Cartesian) -> float:
        electric_potential: float
        try:
            electric_potential = ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point)
        except ZeroDivisionError:
            electric_potential = self.charge * inf
        return electric_potential

    def copy(self) -> PointCharge:
        return PointCharge(self.charge, self.position)


class FiniteLineCharge:
    def __init__(self, charge: float, endpoint_1: Cartesian, endpoint_2: Cartesian) -> None:
        self.charge = charge
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2

    def electric_field(self, point: Cartesian) -> Cartesian:
        distance_endpoint_1: float = self.endpoint_1.distance(point)
        distance_endpoint_2: float = self.endpoint_2.distance(point)

        try:
            inverse_distance_endpoint_1: float = 1 / distance_endpoint_1
            inverse_distance_endpoint_2: float = 1 / distance_endpoint_2
        except ZeroDivisionError:
            return Cartesian(0, 0)

        endpoints: Cartesian = self.endpoint_2.copy().subtract(self.endpoint_1)
        distance_endpoints: float = endpoints.length()
        charge_density: float = self.charge / distance_endpoints
        electric_field_parallel: float = ELECTROSTATIC_CONSTANT * charge_density * (
                inverse_distance_endpoint_1 - inverse_distance_endpoint_2)

        displacement_projection_endpoint_1: float = endpoints.dot_product(
            self.endpoint_1.copy().subtract(point)) / distance_endpoints
        displacement_projection_endpoint_2: float = displacement_projection_endpoint_1 + distance_endpoints
        distance_projection: float = sqrt(distance_endpoint_1 ** 2 - displacement_projection_endpoint_1 ** 2)

        try:
            electric_field_perpendicular: float = ELECTROSTATIC_CONSTANT * charge_density / distance_projection * (
                    displacement_projection_endpoint_2 * inverse_distance_endpoint_2 -
                    displacement_projection_endpoint_1 * inverse_distance_endpoint_1)
        except ZeroDivisionError:
            if displacement_projection_endpoint_1 > 0 or displacement_projection_endpoint_2 < 0:
                electric_field_perpendicular = 0
            else:
                return Cartesian(0, 0)


class InfiniteLineCharge:
    def __init__(self, charge_density: float, point_1: Cartesian, point_2: Cartesian) -> None:
        self.charge_density = charge_density
        self.point_1 = point_1
        self.point_2 = point_2

    def electric_field(self, point: Cartesian) -> Cartesian:
        infinite_line: Cartesian = self.point_2.copy().subtract(self.point_1)
        cross_product: float = infinite_line.cross_product(point.copy().subtract(self.point_1))
        distance_from_infinite_line_to_point: float = abs(cross_product) / infinite_line.length()
        electric_field_intensity: float = 2 * ELECTROSTATIC_CONSTANT * self.charge_density / distance_from_infinite_line_to_point
        electric_field: Cartesian = Cartesian(-infinite_line.y, infinite_line.x).multiply(
            electric_field_intensity).divide(distance_from_infinite_line_to_point)
        if cross_product < 0:
            electric_field.invert()
        return electric_field


class Cartesian:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def change(self, point: Cartesian) -> Cartesian:
        self.x = point.x
        self.y = point.y
        return self

    def replace(self, x, y) -> Cartesian:
        self.x = x
        self.y = y
        return self

    def add(self, point: Cartesian) -> Cartesian:
        self.x += point.x
        self.y += point.y
        return self

    def subtract(self, point: Cartesian) -> Cartesian:
        self.x -= point.x
        self.y -= point.y
        return self

    def multiply(self, multiplier: float) -> Cartesian:
        self.x *= multiplier
        self.y *= multiplier
        return self

    def divide(self, divisor: float) -> Cartesian:
        self.x /= divisor
        self.y /= divisor
        return self

    def invert(self) -> Cartesian:
        self.x = -self.x
        self.y = -self.y
        return self

    def length(self) -> float:
        return hypot(self.x, self.y)

    def distance(self, point: Cartesian) -> float:
        return hypot(self.x - point.x, self.y - point.y)

    def angle(self, point: Cartesian) -> float:
        return atan2(point.y - self.y, point.x - self.x) % tau

    def dot_product(self, point: Cartesian) -> float:
        return self.x * point.x + self.y * point.y

    def cross_product(self, point: Cartesian) -> float:
        return self.x * point.y - self.y * point.x

    def copy(self) -> Cartesian:
        return Cartesian(self.x, self.y)

    def polar(self) -> Polar:
        return Polar(sqrt(self.x ** 2 + self.y ** 2), atan2(self.y, self.x) % tau)


class Polar:
    r: float
    t: float

    def __init__(self, r: float, t: float) -> None:
        self.r = r
        self.t = t

    def change(self, point: Polar) -> Polar:
        self.r = point.r
        self.t = point.t
        return self

    def replace(self, r: float, t: float) -> Polar:
        self.r = r
        self.t = t
        return self

    def multiply(self, multiplier: float) -> Polar:
        self.r *= multiplier
        return self

    def divide(self, divisor: float) -> Polar:
        self.r /= divisor
        return self

    def invert(self) -> Polar:
        self.t = (self.t + pi) % tau
        return self

    def copy(self) -> Polar:
        return Polar(self.r, self.t)

    def cartesian(self) -> Cartesian:
        return Cartesian(self.r * cos(self.t), self.r * sin(self.t))

system = System([PointCharge(ELEMENTARY_CHARGE, Cartesian(3, 3)), PointCharge(-ELEMENTARY_CHARGE, Cartesian(4, -2))])

min_x: float = -50.
min_y: float = -50.
max_x: float = 50.
max_y: float = 50.


width = 50
electric_potentials = np.empty((width, width))

values_x = np.linspace(min_x, max_x, width)
values_y = np.linspace(min_y, max_y, width)

for index_x in range(width):
    for index_y in range(width):
        electric_potentials[index_x][index_y] = system.electric_potential(
            Cartesian(values_x[index_x], values_y[index_y]))

X, Y = np.meshgrid(np.linspace(-3, 3, 40), np.linspace(-3, 3, 40))
Z = (1 - X/2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)


fig, ax = plt.subplots()
ax.imshow(electric_potentials)
plt.show()

mycharge = PointCharge(1E-10, Cartesian(3, 3))

print(mycharge.electric_field(Cartesian(1, 2)).x)
