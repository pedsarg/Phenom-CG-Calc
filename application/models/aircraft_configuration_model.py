from dataclasses import dataclass


@dataclass
class ArmValues:
    basic_empty_arm: float
    crew_arm: float
    side_facing_seat_arm: float
    passengers_1_and_2_arm: float
    passengers_3_and_4_arm: float
    belted_toilet_seat_arm: float
    forward_baggage_compartment_arm: float
    lh_aft_cabinet_arm: float
    aft_baggage_compartment_arm: float


@dataclass
class WeightValues:
    basic_empty_weight: float
    maximum_zero_fuel_weight: float


@dataclass
class GraphLimits:
    limit_weight: list[float]
    limit_cg: list[float]
    line_above_weight: list[float]
    line_above_cg: list[float]
    side_line_weight: list[float]
    side_line_cg: list[float]


@dataclass
class AircraftConfiguration:
    arm_values: ArmValues
    weight_values: WeightValues
    graph_limits: GraphLimits


@dataclass
class CGParameters:
    LEMAC : float = 5.325
    MAC : float = 1.64