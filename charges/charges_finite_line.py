try:
    from time import sleep
    from math import isnan
    from points import Point
    from charges import System, FiniteLineCharge
    from render import render_system

    print(
        "This program will show the electric field and potential around a finite line charge."
    )
    sleep(2)
    print("You can enter the total electric charge of the segment.")
    sleep(1)
    print()

    charge = 0.0

    while True:
        print("Charge of rod")
        try:
            charge = float(input("Coulombs: "))
        except:
            continue
        if isnan(charge):
            continue
        break


    system = System([FiniteLineCharge(charge, Point(3, 3), Point(7, 7), 100)])
    print()
    render_system(
        system,
        minimum=Point(0, 0),
        maximum=Point(10, 10),
        title="Electric field and potential around a\nfinite line charge",
    )
except KeyboardInterrupt:
    exit()
