try:
    from time import sleep
    from math import isnan, cos, sin, tau
    from points import Point
    from charges import System, Charge, PointCharge, FiniteLineCharge
    from render import render_system


    def ask_float(message: str) -> float:
        first = True
        while True:
            if not first:
                print("Invalid Value")
            first = False
            try:
                number = float(input(message))
            except ValueError:
                continue
            else:
                if isnan(number):
                    continue
                return number


    def ask_view() -> tuple[Point, Point]:
        print("Please enter the viewport minimum and maximum values.")
        xmin = ask_float("-> Xmin in meters is [?]: ")
        ymin = ask_float("-> Ymin in meters is [?]: ")
        xmax = ask_float("-> Xmax in meters is [?]: ")
        ymax = ask_float("-> Ymax in meters is [?]: ")
        print(
            f"The viewport is set to (in meters) (({xmin:.5f}, {ymin:.5f}) - ({xmax:.5f}, {ymax:.5f}))."
        )
        return Point(xmin, ymin), Point(xmax, ymax)


    def ask_point_charge() -> PointCharge:
        print("Point charge was selected.")
        c = ask_float("-> Charge in Coulombs is [?]: ")
        x = ask_float("-> X in meters is [?]: ")
        y = ask_float("-> Y in meters is [?]: ")
        print(
            f"The position and charge of the point charge is ({x:.5f}m, {y:.5f}m), {c: .5f}C"
        )
        return PointCharge(c, Point(x, y))


    def ask_finite_line_charge() -> FiniteLineCharge:
        print("Finite line charge was selected.")
        c = ask_float("-> Charge in Coulombs is [?]: ")
        x1 = ask_float("-> X1 in meters is [?]: ")
        y1 = ask_float("-> Y1 in meters is [?]: ")
        x2 = ask_float("-> X2 in meters is [?]: ")
        y2 = ask_float("-> Y2 in meters is [?]: ")
        print(
            f"The positions and charge of the finite line charge is \n(({x1:.5f}m, {y1:.5f}m), ({x2:.5f}m, {y2:.5f}m)), {c: .5f}C"
        )
        return FiniteLineCharge(c, Point(x1, y1), Point(x2, y2), 100)


    def ask_circle_charge() -> list[PointCharge]:
        print("Circle charge was selected.")
        c = ask_float("-> Total charge in Coulombs is [?]: ")
        xc = ask_float("-> Xc in meters is [?]: ")
        yc = ask_float("-> Yc in meters is [?]: ")
        r = ask_float("-> R in meters is [?]: ")
        charges = []
        for n in range(100):
            angle = tau * (n / 100)
            radius = r
            point = Point(xc + radius * cos(angle), yc + radius * sin(angle))
            charges.append(PointCharge(c / 100, point))
        return charges


    all_charges: list[Charge] = []

    print(
        "This program will show the electric field and potential around the user described set of charges.\n"
    )
    sleep(3)

    minimum, maximum = ask_view()

    while True:
        print("Please select what type of charge you would like to add:")
        print("-> [N] - No Charge")
        print("-> [P] - Point Charge")
        print("-> [L] - Finite Line Charge")
        print("-> [C] - Circle of Charge")

        again = False
        while True:
            letter = input("Charge Type [?]: ").upper()
            if letter == "N" or letter == "P" or letter == "L" or letter == "C":
                break
            again = True

        if again:
            continue

        # here
        if letter == "N":
            break
        elif letter == "P":
            point_charge = ask_point_charge()
            all_charges.append(point_charge)
        elif letter == "L":
            finite_line_charge = ask_finite_line_charge()
            all_charges.append(finite_line_charge)
        elif letter == "C":
            circle_charge = ask_circle_charge()
            all_charges.extend(circle_charge)
    try:
        system = System(all_charges)
    except:
        print("Unfortunately, there was an error in the building of the system of charges.")
    else:
        try:
            render_system(
                system,
                minimum=minimum,
                maximum=maximum,
                title="Electric field and potential",
            )
        except:
            print(
                "Unfortunately, there was an error in the displaying of electric field and potential figures."
            )
except KeyboardInterrupt:
    exit()
