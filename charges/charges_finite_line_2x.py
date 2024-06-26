try:
    from time import sleep
    from math import isnan
    from points import Point
    from charges import System, FiniteLineCharge
    from render import render_system

    print(
        "This program will show the electric field and potential around two finite line charges."
    )
    sleep(2)
    print("You can enter the total electric charges of each of the segments.")
    sleep(2.5)
    print()

    charge_1 = 0.0
    charge_2 = 0.0

    while True:
        print("Charge of left rod")
        try:
            charge_1 = float(input("Coulombs: "))
        except:
            continue
        if isnan(charge_1):
            continue
        break

    while True:
        print("Charge of right rod")
        try:
            charge_2 = float(input("Coulombs: "))
        except:
            continue
        if isnan(charge_2):
            continue
        break


    system = System(
        [
            FiniteLineCharge(charge_1, Point(3, 3), Point(3, 7), 100),
            FiniteLineCharge(charge_2, Point(7, 3), Point(7, 7), 100),
        ]
    )
    print()
    render_system(
        system,
        minimum=Point(0, 0),
        maximum=Point(10, 10),
        title="Electric field and potential around\ntwo finite line charges",
    )
except KeyboardInterrupt:
    exit()
