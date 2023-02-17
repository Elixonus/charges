from time import sleep
from math import isnan, cos, sin, tau
from points import Point
from charges import System, PointCharge, FiniteLineCharge
from render import render_system


def ask_float(message: str) -> float:
    first = True
    while True:
        if not first:
            print("Invalid Value")
        first = False
        try:
            number = float(input(message))
        except ValueError:
            continue
        else:
            if isnan(number):
                continue
            return number


def ask_view() -> (Point, Point):
    print("Please enter the viewport minimum and maximum values.")
    xmin = ask_float("Xmin in meters is [?]: ")
    ymin = ask_float("Ymin in meters is [?]: ")
    xmax = ask_float("Xmax in meters is [?]: ")
    ymax = ask_float("Ymax in meters is [?]: ")
    print(f"The viewport is set to (in meters) (({xmin:.5f}, {ymin:.5f}) - ({xmax:.5f}, {ymax:.5f})).")
    return Point(xmin, ymin), Point(xmax, ymax)

def ask_point_charge() -> PointCharge:
    print("Point charge was selected.")
    x = ask_float("X in meters is [?]: ")
    y = ask_float("Y in meters is [?]: ")
    c = ask_float("Charge in Coulombs is [?]: ")
    print(f"The position and charge of the point charge is ({x:.5f}m, {y:.5f}m), {c: .5f}C")
    return PointCharge(c, Point(x, y))

all_charges = []

print("This program will show the electric field and potential around the user described set of charges.\n")
sleep(3)

minimum, maximum = ask_view()

while True:
    print("Please select what type of charge you would like to add:")
    print("[N] - No Charge")
    print("[P] - Point Charge")
    print("[L] - Finite Line Charge")
    print("[C] - Circle of Charge")
    print("[S] - Square of Charge")

    again = False
    while True:
        letter = input("Charge Type [?]: ").upper()
        if letter == "N" or letter == "P" or letter == "L" or letter == "C" or letter == "S":
            break
        again = True

    if again:
        continue

    # here
    if letter == "N":
        break

    elif letter == "P":
        charge = ask_point_charge()
        all_charges.append(charge)

    elif letter == "L":
        print("Finite line charge was selected")
    elif letter == "C":
        print("Circle charge was selected")
    elif letter == "S":
        print("Square charge was selected")

try:
    system = System(all_charges)
except:
    print("Unfortunately, there was an error in the building of the system of charges.")
else:
    try:
        render_system(system, minimum=minimum, maximum=maximum, title="Electric field and potential")
    except:
        print("Unfortunately, there was an error in the displaying of electric field and potential figures.")
