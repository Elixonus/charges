"""Python module for finding electric field and potential of a system of charges."""

from __future__ import annotations
from math import atan2, tau
from collections.abc import Iterator
from points import Point

ELECTROSTATIC_CONSTANT: float = 8.9875517923E+9
"""Electrostatic constant in Newtons, meters squared per Coulombs squared."""
ELEMENTARY_CHARGE: float = 1.602176634E-19
"""Charge of basic unit in Coulombs."""
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

    def __init__(self) -> None:
        """Create a generic charge object, not meant to be called directly."""

    def field(self, point: Point, /) -> Point:
        """Calculation of electric field, that all charges inheriting this class should implement."""
        raise NotImplementedError

    def potential(self, point: Point, /) -> float:
        """Calculation of electric potential, that all charges inheriting this class should implement."""
        raise NotImplementedError


class PointCharge(Charge):
    """Point charge."""
    charge: float
    point: Point

    def __init__(self, charge: float, point: Point) -> None:
        """Create a point charge."""
        super().__init__()
        self.charge = charge
        self.point = point

    def field(self, point: Point, /) -> Point:
        """Calculate the electric field at the specified point."""
        try:
            field = ELECTROSTATIC_CONSTANT * self.charge / self.point.dist(point) ** 3 * (point - self.point)
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


class LineCharge(Charge):
    charge_density: float
    point_1: Point
    point_2: Point

    def __init__(self, charge_density: float, point_1: Point, point_2: Point) -> None:
        super().__init__()
        self.charge_density = charge_density
        self.point_1 = point_1
        self.point_2 = point_2

    def field(self, point: Point, /) -> Point:
        line = self.point_2 - self.point_1
        closest = self.point_1 + (line @ (point - self.point_1) / self.point_1.dist(self.point_2) ** 2) * line
        field = 2 * ELECTROSTATIC_CONSTANT * self.charge_density / point.dist(closest) ** 2 * (point - closest)
        return field

    def potential(self, point: Point, /) -> float:
        pass

"""
class LineCharge(Charge):
    charge_density: float
    point_1: Point
    point_2: Point

    def __init__(self, charge_density: float, point_1: Point, point_2: Point) -> None:
        super().__init__()
        self.charge_density = charge_density
        self.point_1 = point_1
        self.point_2 = point_2

    def field(self, point: Point, /) -> Point:
        line = atan2(self.point_1.y - self.point_2.y, self.point_1.x - self.point_2.x)

        line = (self.point_2 - self.point_1) / self.point_1.dist(self.point_2)

        line_point = self.point_1 + (line @ (point - self.point_1)) * line
        coef = 2 * ELECTROSTATIC_CONSTANT * self.charge_density

        vector = (line_point - point).div(point.dist(line_point))
        return line_point / line_point.len()



    def potential(self, point: Point, /) -> float:
        pass

"""