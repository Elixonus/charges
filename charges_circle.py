from time import sleep
from math import isnan, cos, sin, tau
from points import Point
from charges import System, PointCharge
from render import render_system

print("This program will show the electric field and potential around a uniformly distributed circle of charge.")
sleep(2)
print("You can enter the total electric charge of the circle.")
sleep(1.5)
print()

charge = 0

while True:
    print("Total charge of circle")
    try:
        charge = float(input("Coulombs: "))
    except:
        continue
    if isnan(charge):
        continue
    break

charges = []
for n in range(100):
    angle = tau * (n / 100)
    radius = 3
    point = Point(5 + radius * cos(angle),
                  5 + radius * sin(angle))
    charges.append(PointCharge(charge / 100, point))

system = System(charges)
print()
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric field and potential around\na circle of charge")