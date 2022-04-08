from points import Point
from charges import System, PointCharge, PROTON_CHARGE
from render import render_system

system = System([PointCharge(charge=PROTON_CHARGE, point=Point(5, 5))])
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric potential around a proton")