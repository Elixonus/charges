try:
    from time import sleep
    from points import Point
    from charges import System, PointCharge, PROTON_CHARGE
    from render import render_system

    print(
        "This program will show the electric field and potential around a positive charge."
    )
    sleep(2)

    system = System([PointCharge(charge=PROTON_CHARGE, point=Point(5, 5))])
    print()
    render_system(
        system,
        minimum=Point(0, 0),
        maximum=Point(10, 10),
        title="Electric field and potential around a proton",
    )
except KeyboardInterrupt:
    exit()
