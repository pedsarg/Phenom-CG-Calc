import json
import math

from pathlib import Path
from models.aircraft_configuration_model import AircraftConfiguration, ArmValues, WeightValues, GraphLimits

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_VALUES_PATH = (
    BASE_DIR / "storage/Phenom100e/defaultValues.json"
)

FUEL_TABLE_PATH = (
    BASE_DIR / "storage/Phenom100e/fuelTable.json"
)

def _loadJson(path: Path) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        raise RuntimeError(f"Configuration file not found: {path}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON file: {path}") from e


def getAircraftConfiguration() -> AircraftConfiguration:

    data = _loadJson(DEFAULT_VALUES_PATH)

    if not data:
        raise RuntimeError("Could not load aircraft configuration")

    arm_data = data["armValues"]
    weight_data = data["weightValues"]
    graph_data = data["graphLimits"]

    return AircraftConfiguration(
        arm_values=ArmValues(
            basic_empty_arm=arm_data["basic_empty_arm"],
            crew_arm=arm_data["crew_arm"],
            side_facing_seat_arm=arm_data["side_facing_seat_arm"],
            passengers_1_and_2_arm=arm_data["passengers_1_and_2_arm"],
            passengers_3_and_4_arm=arm_data["passengers_3_and_4_arm"],
            belted_toilet_seat_arm=arm_data["belted_toilet_seat_arm"],
            forward_baggage_compartment_arm=arm_data["forward_baggage_compartment_arm"],
            lh_aft_cabinet_arm=arm_data["lh_aft_cabinet_arm"],
            aft_baggage_compartment_arm=arm_data["aft_baggage_compartment_arm"]
        ),

        weight_values=WeightValues(
            basic_empty_weight=weight_data["basic_empty_weight"],
            maximum_zero_fuel_weight=weight_data["maximum_zero_fuel_weight"]
        ),

        graph_limits=GraphLimits(
            limit_weight=graph_data["limit_weight"],
            limit_cg=graph_data["limit_cg"],
            line_above_weight=graph_data["line_above_weight"],
            line_above_cg=graph_data["line_above_cg"],
            side_line_weight=graph_data["side_line_weight"],
            side_line_cg=graph_data["side_line_cg"]
        )
    )



def getFuelArm(fuelWeight: float) -> float | None:
    data = _loadJson(FUEL_TABLE_PATH)
    
    if not data:
        return None
    
    if fuelWeight <= 20:
        return data["20"]
    
    if fuelWeight >= 1273:
        return data["1273"]
    
    fuelWeightAdjusted = math.floor(fuelWeight / 20) * 20
    return data.get(str(fuelWeightAdjusted))


