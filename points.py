from __future__ import annotations
from math import atan2, cos, hypot, pi, sin, sqrt, tau


class Cartesian:
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def change(self, point: Cartesian, /) -> Cartesian:
        self.x = point.x
        self.y = point.y
        return self

    def replace(self, x, y) -> Cartesian:
        self.x = x
        self.y = y
        return self

    def add(self, point: Cartesian, /) -> Cartesian:
        self.x += point.x
        self.y += point.y
        return self

    def subtract(self, point: Cartesian, /) -> Cartesian:
        self.x -= point.x
        self.y -= point.y
        return self

    def multiply(self, multiplier: float, /) -> Cartesian:
        self.x *= multiplier
        self.y *= multiplier
        return self

    def divide(self, divisor: float, /) -> Cartesian:
        self.x /= divisor
        self.y /= divisor
        return self

    def normalize(self) -> Cartesian:
        return self.divide(self.length())

    def invert(self) -> Cartesian:
        self.x = -self.x
        self.y = -self.y
        return self

    def length(self) -> float:
        return hypot(self.x, self.y)

    def distance(self, point: Cartesian, /) -> float:
        return hypot(self.x - point.x, self.y - point.y)

    def angle(self, point: Cartesian, /) -> float:
        return atan2(point.y - self.y, point.x - self.x) % tau

    def dot_product(self, point: Cartesian, /) -> float:
        return self.x * point.x + self.y * point.y

    def cross_product(self, point: Cartesian, /) -> float:
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

    def change(self, point: Polar, /) -> Polar:
        self.r = point.r
        self.t = point.t
        return self

    def replace(self, r: float, t: float) -> Polar:
        self.r = r
        self.t = t
        return self

    def multiply(self, multiplier: float, /) -> Polar:
        self.r *= multiplier
        return self

    def divide(self, divisor: float, /) -> Polar:
        self.r /= divisor
        return self

    def invert(self) -> Polar:
        self.t = (self.t + pi) % tau
        return self

    def copy(self) -> Polar:
        return Polar(self.r, self.t)

    def cartesian(self) -> Cartesian:
        return Cartesian(self.r * cos(self.t), self.r * sin(self.t))
