from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from points import Point
from charges import System, PointCharge, FiniteLineCharge, ELEMENTARY_CHARGE, PROTON_CHARGE, ELECTRON_CHARGE
from render import render_system

MAP_MINIMUM_X: float = 0.
MAP_MINIMUM_Y: float = 0.
MAP_MAXIMUM_X: float = 10.
MAP_MAXIMUM_Y: float = 10.
MAP_RANGE_X: float = MAP_MAXIMUM_X - MAP_MINIMUM_X
MAP_RANGE_Y: float = MAP_MAXIMUM_Y - MAP_MINIMUM_Y
MAP_LENGTH: int = 100


system = System([
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(5, 5)),
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
    PointCharge(9 * ELEMENTARY_CHARGE, Point(4, 7)),
    PointCharge(ELECTRON_CHARGE, Point(4, 4))
])

render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), size=500)