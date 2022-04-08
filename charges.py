"""Python module for finding electric field and potential of a system of charges."""

from __future__ import annotations
from abc import ABC, abstractmethod
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
        field = Point(0, 0, 0)
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


class Charge(ABC):
    """Generic charge object which all charge classes inherit from."""
    charge: float

    def __init__(self, charge: float) -> None:
        """Create a generic charge object, not meant to be called directly."""
        self.charge = charge

    @abstractmethod
    def field(self, point: Point, /) -> Point:
        """Calculation of electric field, that all charges inheriting this class should implement."""
        pass

    @abstractmethod
    def potential(self, point: Point, /) -> float:
        """Calculation of electric potential, that all charges inheriting this class should implement."""
        pass


class PointCharge(Charge):
    """Point charge."""
    point: Point

    def __init__(self, charge: float, point: Point) -> None:
        """Create a point charge."""
        super().__init__(charge)
        self.charge = charge
        self.point = point

    def field(self, point: Point, /) -> Point:
        """Calculate the electric field at the specified point."""
        try:
            field = (ELECTROSTATIC_CONSTANT * self.charge / self.point.dist(point) ** 2) * (point - self.point).norm()
        except ZeroDivisionError:
            field = Point(0, 0, 0)
        return field

    def potential(self, point: Point, /) -> float:
        """Calculate the electric potential at the specified point."""
        try:
            potential = ELECTROSTATIC_CONSTANT * self.charge / self.point.dist(point)
        except ZeroDivisionError:
            potential = 0
        return potential


class FiniteLineCharge(Charge):
    """Finite line charge."""
    point_charges: list[PointCharge]
    point_1: Point
    point_2: Point

    def __init__(self, charge: float, point_1: Point, point_2: Point, number_point_charges: int) -> None:
        super().__init__(charge)
        self.charge = charge
        self.point_1 = point_1
        self.point_2 = point_2
        self.point_charges = []
        for n in range(number_point_charges):
            ratio = n / (number_point_charges - 1)
            point = ratio * point_1 + (1 - ratio) * point_2
            point_charge = PointCharge(charge / number_point_charges, point)
            self.point_charges.append(point_charge)

    def field(self, point: Point, /) -> Point:
        field = Point(0, 0)
        for point_charge in self.point_charges:
            field += point_charge.field(point)
        return field

    def potential(self, point: Point, /) -> float:
        potential = 0
        for point_charge in self.point_charges:
            potential += point_charge.potential(point)
        return potential
