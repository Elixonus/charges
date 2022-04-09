import matplotlib.pyplot as plt
from charges import System, Point


def render_system(system: System, minimum: Point, maximum: Point, title: str, size: int = 500) -> None:
    difference = maximum - minimum
    potentials = [[system.potential(Point(
        minimum.x + difference.x * (x / (size - 1)),
        minimum.y + difference.y * (y / (size - 1))
    )) for x in range(size)] for y in range(size)]
    potentials_sorted = sorted(potential for potentials_buffer in potentials for potential in potentials_buffer)
    potential_low = potentials_sorted[round(0.05 * (len(potentials_sorted) - 1))]
    potential_high = potentials_sorted[round(0.95 * (len(potentials_sorted) - 1))]
    percentiles = [((n / 99) * 0.98) + 0.01 for n in range(100)]
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
    ax.set_title(title)
    ax.set_xlabel("Horizontal displacement (meters)")
    ax.set_ylabel("Vertical displacement (meters)")
    ax.set_aspect("equal")
    cbar = plt.colorbar(contourf)
    cbar.set_label("Joules per coulomb (Volts)")
    plt.show()


if __name__ == "__main__":
    from time import sleep
    print("This python file is just a library, feel free to try out the other programs.")
    sleep(5)