from constants.aircraft_constants import LEMAC, MAC
from models.flight_model import Moments, BalanceData, WeightAndBalance
from models.aircraft_configuration_model import WeightValues, ArmValues


def calculateMoments(balance_data: BalanceData, weights: WeightValues, arms: ArmValues) -> Moments:
    return Moments(
        basic_empty_moment  =arms.basic_empty_arm * weights.basic_empty_weight,
        crew_moment = arms.crew_arm * balance_data.crew_weight,
        side_facing_seat_moment=arms.side_facing_seat_arm * balance_data.side_facing_seat_weight,
        passengers_1_and_2_moment=arms.passengers_1_and_2_arm * balance_data.passengers_1_and_2_weight,
        passengers_3_and_4_moment=arms.passengers_3_and_4_arm * balance_data.passengers_3_and_4_weight,
        belted_toilet_seat_moment=arms.belted_toilet_seat_arm * balance_data.belted_toilet_seat_weight,
        forward_baggage_moment=arms.forward_baggage_compartment_arm * balance_data.forward_baggage_compartment_weight,
        lh_aft_cabinet_moment=arms.lh_aft_cabinet_arm * balance_data.lh_aft_cabinet_weight,
        aft_baggage_moment=arms.aft_baggage_compartment_arm * balance_data.aft_baggage_compartment_weight,
    )


def calculateAdjustedZeroFuel(balance_data: BalanceData, weights: WeightValues, moments: Moments) -> WeightAndBalance:

    weight = (
        weights.basic_empty_weight +
        balance_data.crew_weight +
        balance_data.side_facing_seat_weight +
        balance_data.passengers_1_and_2_weight +
        balance_data.passengers_3_and_4_weight +
        balance_data.belted_toilet_seat_weight +
        balance_data.forward_baggage_compartment_weight +
        balance_data.lh_aft_cabinet_weight +
        balance_data.aft_baggage_compartment_weight
    )

    moment = (
        moments.basic_empty_moment +
        moments.crew_moment +
        moments.side_facing_seat_moment +
        moments.passengers_1_and_2_moment +
        moments.passengers_3_and_4_moment +
        moments.belted_toilet_seat_moment +
        moments.forward_baggage_moment +
        moments.lh_aft_cabinet_moment +
        moments.aft_baggage_moment
    )

    if weight <= 0:
        raise ValueError("Weight must be greater than zero")

    return WeightAndBalance(
        weight=weight,
        arm = moment / weight,
        moment=moment,
    )


def calculateFuelMoment(fuel_arm : float, fuel_weight : float) -> float:
    return fuel_arm * fuel_weight


def calculateWeightAndBalance(weight_and_balance: WeightAndBalance, fuel_weight: float, fuel_moment: float) -> WeightAndBalance:
    weight = weight_and_balance.weight + fuel_weight
    moment = weight_and_balance.moment + fuel_moment
    
    if weight <= 0:
        raise ValueError("Weight must be greater than zero")

    return WeightAndBalance(
        weight = weight,
        moment = moment,
        arm    = moment / weight
    )


def convertArmToCGPercent(arm: float) -> float:
    return (((arm - LEMAC) / MAC) * 100)
