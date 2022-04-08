from time import sleep
from points import Point
from charges import System, PointCharge, PROTON_CHARGE, ELECTRON_CHARGE
from render import render_system

print("This program will show the electric potential around three point charges.")
sleep(2)
print("You can enter the electric charge in Coulombs of each particle.")
sleep(2)



system = System([PointCharge(charge=PROTON_CHARGE, point=Point(2, 5)),
                 PointCharge(charge=ELECTRON_CHARGE, point=Point(8, 5)),
                 PointCharge(charge=ELECTRON_CHARGE, point=Point(4, 6))])
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric potential around three points charges")