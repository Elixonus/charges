from __future__ import annotations
from math import atan2, cos, hypot, inf, pi, sin, sqrt, tau
from typing import Iterator
import points as pt

ELECTROSTATIC_CONSTANT: float = 8.9875517923E+9
ELEMENTARY_CHARGE: float = 1.602176634E-19
PROTON_CHARGE: float = ELEMENTARY_CHARGE
ELECTRON_CHARGE: float = -ELEMENTARY_CHARGE
NEUTRAL_CHARGE: float = 0.


class System:
    charges: list[PointCharge]

    def __init__(self, *charges: PointCharge) -> None:
        self.charges = list(charges)

    def electric_field(self, point: pt.Cartesian, /) -> pt.Cartesian:
        electric_field: pt.Cartesian = pt.Cartesian(0, 0)
        for charge in self.charges:
            electric_field.add(charge.electric_field(point))
        return electric_field

    def electric_fields(self, point: pt.Cartesian, /) -> Iterator[pt.Cartesian]:
        for charge in self.charges:
            electric_field: pt.Cartesian = charge.electric_field(point)
            yield electric_field

    def electric_potential(self, point: pt.Cartesian, /) -> float:
        electric_potential: float = 0.
        for charge in self.charges:
            electric_potential += charge.electric_potential(point)
        return electric_potential

    def electric_potentials(self, point: pt.Cartesian, /) -> Iterator[float]:
        for charge in self.charges:
            electric_potential: float = charge.electric_potential(point)
            yield electric_potential

    def copy(self) -> System:
        return System(*self.charges)


class PointCharge:
    charge: float
    position: pt.Cartesian

    def __init__(self, charge: float, position: pt.Cartesian) -> None:
        self.charge = charge
        self.position = position

    def electric_field(self, point: pt.Cartesian, /) -> pt.Cartesian:
        electric_field: pt.Cartesian
        try:
            electric_field = pt.Polar(ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point) ** 2, self.position.angle(point)).cartesian()
        except ZeroDivisionError:
            electric_field = pt.Cartesian(0, 0)
        return electric_field

    def electric_potential(self, point: pt.Cartesian, /) -> float:
        electric_potential: float
        try:
            electric_potential = ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point)
        except ZeroDivisionError:
            electric_potential = self.charge * inf
        return electric_potential

    def copy(self) -> PointCharge:
        return PointCharge(self.charge, self.position)


"""
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
"""




system = System(PointCharge(1, pt.Cartesian(1, 0)), PointCharge(-1, pt.Cartesian(0, 1)))
print(system.electric_potentials(pt.Cartesian(0, 0)))