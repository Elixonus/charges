from __future__ import annotations
from points import Point
from charges import System, PointCharge, ELEMENTARY_CHARGE, PROTON_CHARGE, ELECTRON_CHARGE
from structures import CircleStructure

MAP_MINIMUM_X: float = 0.
MAP_MINIMUM_Y: float = 0.
MAP_MAXIMUM_X: float = 10.
MAP_MAXIMUM_Y: float = 10.
MAP_RANGE_X: float = MAP_MAXIMUM_X - MAP_MINIMUM_X
MAP_RANGE_Y: float = MAP_MAXIMUM_Y - MAP_MINIMUM_Y
MAP_LENGTH: int = 200


electric_system: System = System([
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(5, 5)),
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
    PointCharge(5 * ELEMENTARY_CHARGE, Point(5, 7)),
    PointCharge(ELECTRON_CHARGE, Point(4, 4)),
    CircleStructure(10 * ELEMENTARY_CHARGE, Point(4, 5), 1, 50)
])

electric_potentials: list[list[float]] = [[electric_system.potential(Point(
    MAP_MINIMUM_X + MAP_RANGE_X * (map_x / (MAP_LENGTH - 1)),
    MAP_MINIMUM_Y + MAP_RANGE_Y * (map_y / (MAP_LENGTH - 1))
)) for map_y in range(MAP_LENGTH)] for map_x in range(MAP_LENGTH)]
