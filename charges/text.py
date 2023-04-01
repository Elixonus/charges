from math import sqrt
from random import choice, randint
from string import ascii_letters
from rich.console import Console
from charges import System
from points import Point

console = Console()


def text_system(
    system: System, minimum: Point, maximum: Point, potential_size: int = 10
) -> None:
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
    potential_low = potentials_sorted[round(0.02 * (len(potentials_sorted) - 1))]
    potential_high = potentials_sorted[round(0.98 * (len(potentials_sorted) - 1))]

    normals = [[0.0 for x in range(potential_size)] for y in range(potential_size)]
    for x in range(potential_size):
        for y in range(potential_size):
            potential = potentials[x][y]
            if potential < 0:
                normal = min(max(-potential / potential_low, -1), 1)
            elif potential > 0:
                normal = min(max(potential / potential_high, -1), 1)
            else:
                normal = 0
            normals[x][y] = normal

    console.print(" " + ("#" * (2 * potential_size + 6)) + " ", style="rgb(60,60,60)")
    console.print("##", end="", style="rgb(60,60,60)")
    console.print("#" * (2 * potential_size + 4), end="", style="rgb(90,90,90)")
    console.print("##", style="rgb(60,60,60)")
    for x in range(potential_size):
        for _ in range(2):
            console.print("#", end="", style="rgb(60,60,60)")
        for _ in range(2):
            console.print("#", end="", style="rgb(90,90,90)")
        for y in range(potential_size):
            normal = normals[-x - 1][y]
            if normal < 0:
                channel = round(255 * (normal + 1))
                color = f"rgb({channel},{channel},{255})"
            elif normal > 0:
                channel = round(255 * (1 - normal))
                color = f"rgb({255},{channel},{channel})"
            else:
                color = "rgb(255,255,255)"
            console.print(
                choice(ascii_letters) + choice(ascii_letters), style=f"{color}", end=""
            )
        for _ in range(2):
            console.print("#", style="rgb(90,90,90)", end="")
        for _ in range(2):
            console.print("#", style="rgb(60,60,60)", end="")
        console.print("")
    console.print("##", end="", style="rgb(60,60,60)")
    console.print("#" * (2 * potential_size + 4), end="", style="rgb(90,90,90)")
    console.print("##", style="rgb(60,60,60)")
    console.print(" " + ("#" * (2 * potential_size + 6)) + " ", style="rgb(60,60,60)")


if __name__ == "__main__":
    from time import sleep

    print(
        "This python file is just a library, feel free to try out the other programs."
    )
    sleep(5)
