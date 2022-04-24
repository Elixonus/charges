from time import sleep
from points import Point
from charges import System, PointCharge, PROTON_CHARGE, ELECTRON_CHARGE
from render_potential import render_system

print("This program will show the electric potential around two oppositely charged particles.")
sleep(2)

system = System([PointCharge(charge=PROTON_CHARGE, point=Point(2, 5)),
                 PointCharge(charge=ELECTRON_CHARGE, point=Point(8, 5))])
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric potential around a proton and an electron")