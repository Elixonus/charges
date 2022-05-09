from time import sleep
from math import isnan
from points import Point
from charges import System, FiniteLineCharge
from render import render_system

print("This program will show the electric field and potential around a uniformly distributed square of charge.")
sleep(2)
print("You can enter the total electric charge of the square.")
sleep(1.5)
print()

charge = 0

while True:
    print("Total charge of square")
    try:
        charge = float(input("Coulombs: "))
    except:
        continue
    if isnan(charge):
        continue
    break


system = System([FiniteLineCharge(charge / 4, Point(3, 7), Point(7, 7), 100),
                 FiniteLineCharge(charge / 4, Point(7, 7), Point(7, 3), 100),
                 FiniteLineCharge(charge / 4, Point(7, 3), Point(3, 3), 100),
                 FiniteLineCharge(charge / 4, Point(3, 3), Point(3, 7), 100)])
print()
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric field and potential around\na square of charge")