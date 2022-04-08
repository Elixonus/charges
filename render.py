import matplotlib.pyplot as plt
import numpy as np
from charges import System, PointCharge, FiniteLineCharge, Point


def render_system(system: System, minimum: Point, maximum: Point, title: str, size: int = 500) -> None:
    difference = maximum - minimum
    potentials = [[system.potential(Point(
        minimum.x + difference.x * (x / (size - 1)),
        minimum.y + difference.y * (y / (size - 1))
    )) for y in range(size)] for x in range(size)]
    potentials_sorted = sorted(potential for potentials_buffer in potentials for potential in potentials_buffer)
    potential_low = potentials_sorted[round(0.05 * (len(potentials_sorted) - 1))]
    potential_high = potentials_sorted[round(0.95 * (len(potentials_sorted) - 1))]
    percentiles = np.linspace(0.01, 0.99, 100)
    potentials_interest = [
        potentials_sorted[round(0.01 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.05 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.1 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.2 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.3 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.4 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.5 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.6 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.7 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.8 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.9 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.95 * (len(potentials_sorted) - 1))],
        potentials_sorted[round(0.99 * (len(potentials_sorted) - 1))]
    ]
    fig, ax = plt.subplots()
    contourf = ax.contourf(potentials, cmap="seismic", extent=(minimum.x, maximum.x, minimum.y, maximum.y), levels=potentials_interest, extend="both")
    ax.contour(potentials, extent=(minimum.x, maximum.x, minimum.y, maximum.y), levels=potentials_interest, colors="black", linestyles="solid", linewidths=1)
    cbar = plt.colorbar(contourf)
    plt.xlabel("Horizontal displacement (meters)")
    plt.ylabel("Vertical displacement (meters)")
    cbar.ax.set_ylabel("Joules per coulomb (Volts)")
    plt.title(title)
    plt.show()