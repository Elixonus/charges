from points import Point
from charges import System, PointCharge, FiniteLineCharge, ELEMENTARY_CHARGE, PROTON_CHARGE, ELECTRON_CHARGE
from render import render_system


system = System([
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(5, 5)),
    PointCharge(-5 * ELEMENTARY_CHARGE, Point(7, 5)),
    PointCharge(9 * ELEMENTARY_CHARGE, Point(4, 7)),
    PointCharge(ELECTRON_CHARGE, Point(4, 4))
])

render_system(system, minimum=Point(0, 0), maximum=Point(10, 10), title="Electric potential", size=500)