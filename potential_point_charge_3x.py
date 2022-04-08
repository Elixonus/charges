from points import Point
from charges import System, PointCharge, PROTON_CHARGE, ELECTRON_CHARGE
from render import render_system


system = System([PointCharge(charge=PROTON_CHARGE, point=Point(2, 5)),
                 PointCharge(charge=ELECTRON_CHARGE, point=Point(8, 5)),
                 PointCharge(charge=ELECTRON_CHARGE, point=Point(4, 6))])
render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric potential around three points charges")