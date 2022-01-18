"""Python module for finding electric field and potential of a system of charges."""

from __future__ import annotations
from math import atan2
from collections.abc import Iterator
from points import Point

ELECTROSTATIC_CONSTANT: float = 8.9875517923E+9
"""Electrostatic constant in Newtons, meters squared per Coulombs squared."""
ELEMENTARY_CHARGE: float = 1.602176634E-19
"""Basic unit of charge in Coulombs."""
PROTON_CHARGE: float = ELEMENTARY_CHARGE
"""Charge of a proton in Coulombs."""
ELECTRON_CHARGE: float = -ELEMENTARY_CHARGE
"""Charge of an electron in Coulombs."""
NEUTRON_CHARGE: float = 0
"""Charge of a neutron in Coulombs."""


class System:
    """System of charges."""
    charges: list[Charge]

    def __init__(self, charges: list[Charge]) -> None:
        """Create a system of charges."""
        self.charges = charges

    def field(self, point: Point, /) -> Point:
        """Calculate the electric field at the specified point in the system."""
        field = Point(0, 0)
        for charge in self.charges:
            field += charge.field(point)
        return field

    def fields(self, point: Point, /) -> Iterator[Point]:
        """Calculate the independent electric fields caused by each charge at the specified point in the system."""
        for charge in self.charges:
            field = charge.field(point)
            yield field

    def potential(self, point: Point, /) -> float:
        """Calculate the electric potential at the specified point in the system."""
        potential = 0
        for charge in self.charges:
            potential += charge.potential(point)
        return potential

    def potentials(self, point: Point, /) -> Iterator[float]:
        """Calculate the independent electric potentials caused by each charge at the specified point in the system."""
        for charge in self.charges:
            potential = charge.potential(point)
            yield potential


class Charge:
    """Generic charge object which all charge classes inherit from."""
    charge: float

    def __init__(self, charge: float) -> None:
        """Create a generic charge object, not meant to be called directly."""
        self.charge = charge

    def field(self, point: Point, /) -> Point:
        """Calculation of electric field method, that all charges inheriting this class should implement."""
        raise NotImplementedError

    def potential(self, point: Point, /) -> float:
        """Calculation of electric potential method, that all charges inheriting this class should implement."""
        raise NotImplementedError


class PointCharge(Charge):
    """Point charge."""
    point: Point

    def __init__(self, charge: float, point: Point) -> None:
        """Create a point charge."""
        super().__init__(charge)
        self.point = point

    def field(self, point: Point, /) -> Point:
        """Calculate the electric field at the specified point."""
        try:
            field = Point.polar(ELECTROSTATIC_CONSTANT * self.charge / self.point.dist(point) ** 2,
                                atan2(point.y - self.point.y, point.x - self.point.x))
        except ZeroDivisionError:
            field = Point(0, 0)
        return field

    def potential(self, point: Point, /) -> float:
        """Calculate the electric potential at the specified point."""
        try:
            potential = ELECTROSTATIC_CONSTANT * self.charge / self.point.dist(point)
        except ZeroDivisionError:
            potential = 0
        return potential


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
