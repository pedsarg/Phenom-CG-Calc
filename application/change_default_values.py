from dataclasses import asdict, fields
from aircraft_repository import DEFAULT_VALUES_PATH, getAircraftConfiguration
import json


def changeDefaultValues():

    print("\n\n\nChange the default values!")

    print(
        "\n\n Enter the new values for the following fields\n"
        " If you want to keep the current value, just press enter"
    )

    config = getAircraftConfiguration()

    print("\n\n Arm values")

    for field in fields(config.arm_values):

        current_value = getattr(
            config.arm_values,
            field.name
        )

        new_value = input(f"{field.name} ({current_value}): ").strip()

        if new_value:
            setattr(
                config.arm_values,
                field.name,
                float(new_value)
            )

    print("\n\n Weight values")

    for field in fields(config.weight_values):

        current_value = getattr(
            config.weight_values,
            field.name
        )

        new_value = input(f"{field.name} ({current_value}): ").strip()

        if new_value:
            setattr(
                config.weight_values,
                field.name,
                float(new_value)
            )

    print("\n\n Graph values")

    for field in fields(config.graph_limits):

        current_value = getattr(
            config.graph_limits,
            field.name
        )

        while True:

            new_value = input(
                f"{field.name} "
                f"({len(current_value)} values) "
                f"{current_value}: "
            ).strip()

            if not new_value:
                break

            try:

                values = [
                    float(value.strip())
                    for value in new_value.split(",")
                ]

                if len(values) != len(current_value):

                    print(
                        f"Invalid number of values! "
                        f"Expected {len(current_value)} values."
                    )

                    continue

                setattr(
                    config.graph_limits,
                    field.name,
                    values
                )

                break

            except ValueError:

                print(
                    "Invalid format! "
                    "Use: 1, 2, 3"
                )

    changed_values = {
        "armValues": asdict(config.arm_values),
        "weightValues": asdict(config.weight_values),
        "graphLimits": asdict(config.graph_limits)
    }

    with open(DEFAULT_VALUES_PATH, "w") as file:
        json.dump(changed_values, file, indent=4)

    print("\nValues changed successfully!")