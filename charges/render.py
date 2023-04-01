import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from charges import System, Point
from text import text_system


def render_system(
    system: System,
    minimum: Point,
    maximum: Point,
    title: str,
    field_size: int = 20,
    potential_size: int = 100,
) -> None:
    print("Solving electric field and potential equations numerically...")
    difference = maximum - minimum
    potentials = [
        [
            system.potential(
                Point(
                    minimum.x + difference.x * (x / (potential_size - 1)),
                    minimum.y + difference.y * (y / (potential_size - 1)),
                )
            )
            for x in range(potential_size)
        ]
        for y in range(potential_size)
    ]
    potentials_sorted = sorted(
        potential for potentials_buffer in potentials for potential in potentials_buffer
    )
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
        potentials_sorted[round(0.99 * (len(potentials_sorted) - 1))],
    ]
    norm_center = colors.TwoSlopeNorm(vcenter=0)
    fig, ax = plt.subplots()
    contourf = ax.contourf(
        potentials,
        cmap="seismic",
        extent=(minimum.x, maximum.x, minimum.y, maximum.y),
        levels=potentials_interest,
        extend="both",
        norm=norm_center,
    )
    ax.contour(
        potentials,
        extent=(minimum.x, maximum.x, minimum.y, maximum.y),
        levels=potentials_interest,
        colors="black",
        linestyles="solid",
        linewidths=1,
        norm=norm_center,
    )
    x = np.linspace(minimum.x, maximum.x, field_size)
    y = np.linspace(minimum.y, maximum.y, field_size)
    u = np.empty((field_size, field_size))
    v = np.empty((field_size, field_size))
    for a in range(field_size):
        for b in range(field_size):
            field = system.field(Point(x[a], y[b]))
            try:
                field_unit = field / field.len()
            except ZeroDivisionError:
                field_unit = Point(0, 0)
            u[b][a] = field_unit.x
            v[b][a] = field_unit.y
    ax.quiver(x, y, u, v)
    ax.set_title(title)
    ax.set_xlabel("Horizontal displacement (meters)")
    ax.set_ylabel("Vertical displacement (meters)")
    ax.set_aspect("equal")
    cbar = plt.colorbar(contourf)
    cbar.set_label("Joules per coulomb (Volts)")
    print("Done, displaying results...\n")
    text_system(system, minimum, maximum, potential_size=20)
    plt.show()


if __name__ == "__main__":
    from time import sleep

    print(
        "This python file is just a library, feel free to try out the other programs."
    )
    sleep(5)
