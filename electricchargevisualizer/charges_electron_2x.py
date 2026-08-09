try:
    from time import sleep
    from points import Point
    from charges import System, PointCharge, ELECTRON_CHARGE
    from render import render_system

    print(
        "This program will show the electric field and potential around two similarly charged particles."
    )
    sleep(2)

    system = System(
        [
            PointCharge(charge=ELECTRON_CHARGE, point=Point(2, 5)),
            PointCharge(charge=ELECTRON_CHARGE, point=Point(8, 5)),
        ]
    )
    print()
    render_system(
        system,
        minimum=Point(0, 0),
        maximum=Point(10, 10),
        title="Electric field and potential around\ntwo electrons",
    )
except KeyboardInterrupt:
    exit()
