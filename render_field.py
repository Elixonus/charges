import matplotlib.pyplot as plt
import numpy as np
from charges import System, Point


def render_system(system: System, minimum: Point, maximum: Point, title: str, size: int = 500) -> None:
    x = np.linspace(minimum.x, maximum.x, size)
    y = np.linspace(minimum.y, maximum.y, size)
    u = np.empty((size, size))
    v = np.empty((size, size))

    for a in range(size):
        for b in range(size):
            field = system.field(Point(x[a], y[b]))
            u[a][b] = field.x
            v[a][b] = field.y

    color = np.log(np.hypot(v, u))
    fig, ax = plt.subplots()
    ax.streamplot(x, y, v, u, color=color)
    ax.set_title(title)
    ax.set_xlabel("Horizontal displacement (meters)")
    ax.set_ylabel("Vertical displacement (meters)")
    ax.set_aspect("equal")
    plt.show()


if __name__ == "__main__":
    from time import sleep
    print("This python file is just a library, feel free to try out the other programs.")
    sleep(5)