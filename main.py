from __future__ import annotations
from math import atan2, cos, hypot, pi, sin, sqrt, tau

ELECTROSTATIC_CONSTANT: float = 8.9875517923E9


class System:
    def __init__(self, charges: list[PointCharge]) -> None:
        self.charges = charges

    def electric_field(self, point: Cartesian) -> Cartesian:
        electric_field = Cartesian(0, 0)
        for charge in self.charges:
            electric_field.add(charge.electric_field(point).cartesian())
        return electric_field

    def electric_potential(self, point: Cartesian) -> float:
        electric_potential = 0
        for charge in self.charges:
            electric_potential += charge.electric_potential(point)
        return electric_potential


class Charge:
    def __init__(self, charge: float) -> None:
        self.charge = charge


class PointCharge(Charge):
    def __init__(self, charge: float, position: Cartesian) -> None:
        super().__init__(charge)
        self.position = position

    def electric_field(self, point: Cartesian) -> Polar:
        try:
            return Polar(ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point) ** 2,
                         self.position.angle(point))
        except ZeroDivisionError:
            return Polar(0, 0)

    def electric_potential(self, point: Cartesian) -> float:
        try:
            return ELECTROSTATIC_CONSTANT * self.charge / self.position.distance(point)
        except ZeroDivisionError:
            return 0

    def copy(self) -> PointCharge:
        return PointCharge(self.charge, self.position)


class FiniteLineCharge(Charge):
    def __init__(self, charge: float, endpoint_1: Cartesian, endpoint_2: Cartesian) -> None:
        super().__init__(charge)
        self.endpoint_1 = endpoint_1
        self.endpoint_2 = endpoint_2

    def electric_field(self, point: Cartesian) -> Cartesian:
        endpoints: Cartesian = self.endpoint_2.copy().subtract(self.endpoint_1)
        distance_endpoints: float = endpoints.length()
        distance_endpoint_1: float = self.endpoint_1.distance(point)
        distance_endpoint_2: float = self.endpoint_2.distance(point)
        charge_density: float = self.charge / distance_endpoints

        try:
            electric_field_parallel: float = ELECTROSTATIC_CONSTANT * charge_density * (
                    1 / distance_endpoint_1 - 1 / distance_endpoint_2)
        except ZeroDivisionError:
            return Cartesian(0, 0)

        distance_projection_endpoint_1: float = 5
        distance_projection: float


class InfiniteLineCharge(Charge):
    def __init__(self, charge: float, point_1: Cartesian, point_2: Cartesian) -> None:
        super().__init__(charge)
        self.point_1 = point_1
        self.point_2 = point_2


class Cartesian:
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
        return atan2(point.y - self.y, point.x - self.x)

    def dot_product(self, point: Cartesian) -> float:
        return self.x * point.x + self.y * point.y

    def copy(self) -> Cartesian:
        return Cartesian(self.x, self.y)

    def polar(self) -> Polar:
        return Polar(sqrt(self.x ** 2 + self.y ** 2), atan2(self.y, self.x) % tau)


class Polar:
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


charge1 = PointCharge(0.000000005, Cartesian(-5, 0))
charge2 = PointCharge(0.000000005, Cartesian(5, 0))
