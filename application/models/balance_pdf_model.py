from dataclasses import dataclass


@dataclass
class BalanceRow:
    arm: float
    weight: float
    moment: float


@dataclass
class BalanceTableData:
    bew: BalanceRow
    crew: BalanceRow
    side_facing_seat: BalanceRow
    passengers_1_and_2: BalanceRow
    passengers_3_and_4: BalanceRow
    belted_toilet_seat: BalanceRow
    forward_baggage_compartment: BalanceRow
    lh_aft_cabinet: BalanceRow
    aft_baggage_compartment: BalanceRow
    maximum_zero_fuel : float
    adjusted_zero_fuel: BalanceRow
    take_off_fuel: BalanceRow
    airplane_weight_and_balance_takeoff: BalanceRow
    landing_fuel: BalanceRow
    airplane_weight_and_balance_landing: BalanceRow
    take_off_cg: float
    landing_cg: float