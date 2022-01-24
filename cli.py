from time import sleep
from charges import System, PointCharge, Point

print("Welcome to the interactive electric charge command-line interface.")


charges = []

while True:
    print("Select what type of charge you would like to add.")
    print()
    charge_type = input("Type of charge: ")

    match charge_type:
        case "":
            break

        case "Point Charge":
            while True:
                try:
                    charge_charge = float(input("Charge (coulombs): "))
                    break
                except ValueError:
                    pass

            while True:
                try:
                    charge_point_x = float(input("Horizontal displacement (meters): "))
                    break
                except ValueError:
                    pass

            while True:
                try:
                    charge_point_y = float(input("Vertical displacement (meters): "))
                    break
                except ValueError:
                    pass

            charge = PointCharge(charge_charge, Point(charge_point_x, charge_point_y))
        case _:
            continue

    charges.append(charge)

system = System(charges)
print()

while True:
    while True:
        try:
            test_point_x = float(input("Test point horizontal displacement (meters): "))
            break
        except ValueError:
            pass

    while True:
        try:
            test_point_y = float(input("Test point vertical displacement (meters): "))
            break
        except ValueError:
            pass

    test_point = Point(test_point_x, test_point_y)
    test_field = system.field(test_point)
    test_potential = system.potential(test_point)
    print(f"Electric field vector (newtons / coulomb): {test_field.x}, {test_field.y}")
    print(f"Electric potential (joules / coulomb): {test_potential}")
