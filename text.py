from math import sqrt
from random import choice
from string import ascii_letters
from rich.console import Console
from charges import System
from points import Point

console = Console()
# console.print("A", style="rgb(255,0,0)")

def text_system(system: System, minimum: Point, maximum: Point, potential_size: int = 10) -> None:
    difference = maximum - minimum
    potentials = [[system.potential(Point(
        minimum.x + difference.x * (x / (potential_size - 1)),
        minimum.y + difference.y * (y / (potential_size - 1))
    )) for x in range(potential_size)] for y in range(potential_size)]
    potentials_sorted = sorted(potential for potentials_buffer in potentials for potential in potentials_buffer)
    potential_low = potentials_sorted[round(0.1 * (len(potentials_sorted) - 1))]
    potential_high = potentials_sorted[round(0.9 * (len(potentials_sorted) - 1))]

    normals = [[0. for x in range(potential_size)] for y in range(potential_size)]
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

    for x in range(potential_size):
        for y in range(potential_size):
            normal = normals[x][y]
            if normal < 0:
                channel = round(255 * (normal + 1))
                color = f"rgb({channel},{channel},255)"
            elif normal > 0:
                channel = round(255 * (1 - normal))
                color = f"rgb(255,{channel},{channel})"
            else:
                color = "rgb(255,255,255)"
            console.print(choice(ascii_letters) + choice(ascii_letters), style=f"{color}", end="")
        console.print("")