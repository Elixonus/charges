from time import sleep
from math import isnan
from points import Point
from charges import System, PointCharge
from render import render_system

print("This program will show the electric field and potential around three point charges.")
sleep(2)
print("You can enter the electric charge in Coulombs of each particle.")
sleep(2)
print()

charge_1 = 0
charge_2 = 0
charge_3 = 0

while True:
    print("Charge of first particle (left)")
    try:
        charge_1 = float(input("Coulombs: "))
    except:
        continue
    if isnan(charge_1):
        continue
    break

while True:
    print("Charge of second particle (middle)")
    try:
        charge_2 = float(input("Coulombs: "))
    except:
        continue
    if isnan(charge_2):
        continue
    break

while True:
    print("Charge of third particle (right)")
    try:
        charge_3 = float(input("Coulombs: "))
    except:
        continue
    if isnan(charge_3):
        continue
    break

system = System([PointCharge(charge=charge_1, point=Point(2, 5)),
                 PointCharge(charge=charge_2, point=Point(4, 6)),
                 PointCharge(charge=charge_3, point=Point(8, 5))])
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric field and potential around\nthree points charges")