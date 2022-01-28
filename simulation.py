from __future__ import annotations
import matplotlib.pyplot as plt
import numpy as np
from points import Point
from charges import System, PointCharge, ELEMENTARY_CHARGE, PROTON_CHARGE, ELECTRON_CHARGE
from structures import CircleStructure

MAP_MINIMUM_X: float = 0.
MAP_MINIMUM_Y: float = 0.
MAP_MAXIMUM_X: float = 10.
MAP_MAXIMUM_Y: float = 10.
MAP_RANGE_X: float = MAP_MAXIMUM_X - MAP_MINIMUM_X
MAP_RANGE_Y: float = MAP_MAXIMUM_Y - MAP_MINIMUM_Y
MAP_LENGTH: int = 100


electric_system = System([
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(5, 5)),
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
    PointCharge(9 * ELEMENTARY_CHARGE, Point(4, 7)),
    PointCharge(ELECTRON_CHARGE, Point(4, 4))
])

electric_potentials = [[electric_system.potential(Point(
    MAP_MINIMUM_X + MAP_RANGE_X * (map_x / (MAP_LENGTH - 1)),
    MAP_MINIMUM_Y + MAP_RANGE_Y * (map_y / (MAP_LENGTH - 1))
)) for map_y in range(MAP_LENGTH)] for map_x in range(MAP_LENGTH)]

electric_potentials_sorted = sorted(electric_potential for electric_potentials_buffer in electric_potentials for electric_potential in electric_potentials_buffer)
electric_potential_low = electric_potentials_sorted[round(0.05 * (len(electric_potentials_sorted) - 1))]
electric_potential_high = electric_potentials_sorted[round(0.95 * (len(electric_potentials_sorted) - 1))]

percentiles = np.linspace(0.01, 0.99, 100)

electric_potentials_interest = [
    electric_potentials_sorted[round(0.01 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.05 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.1 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.2 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.3 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.4 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.5 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.6 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.7 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.8 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.9 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.95 * (len(electric_potentials_sorted) - 1))],
    electric_potentials_sorted[round(0.99 * (len(electric_potentials_sorted) - 1))],
]


fig, ax = plt.subplots()
ax.contourf(electric_potentials, extent=(MAP_MINIMUM_X, MAP_MAXIMUM_X, MAP_MINIMUM_Y, MAP_MAXIMUM_Y), levels=electric_potentials_interest, extend="both")
ax.contour(electric_potentials, extent=(MAP_MINIMUM_X, MAP_MAXIMUM_X, MAP_MINIMUM_Y, MAP_MAXIMUM_Y), levels=electric_potentials_interest, colors="black", linestyles="solid", linewidths=1)
plt.show()
