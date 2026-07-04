from dataclasses import dataclass
from datetime import date, time

@dataclass
class Passenger:
    name: str
    document: str


@dataclass
class PassengerData:
    passengers: list[Passenger]


@dataclass
class CrewMember:
    name: str
    license_number: str


@dataclass
class Airport:
    location: str
    icao: str


@dataclass
class FlightData:
    log_book_page: int
    flight_date: date
    prefix: str
    model: str
    operator: str
    origin: Airport
    destination: Airport
    take_off_time: time
    landing_time: time
    pilot: CrewMember
    copilot: CrewMember


@dataclass
class BalanceData:
    crew_weight: float
    side_facing_seat_weight: float
    passengers_1_and_2_weight: float
    passengers_3_and_4_weight: float
    belted_toilet_seat_weight: float
    forward_baggage_compartment_weight: float
    lh_aft_cabinet_weight: float
    aft_baggage_compartment_weight: float
    take_off_fuel_weight: float
    landing_fuel_weight: float


@dataclass
class NoteData:
    atis: str
    rto: str
    clearance: str


@dataclass
class CgResult:
    take_off_weight: float
    take_off_moment: float
    take_off_arm: float
    take_off_cg: float
    landing_weight: float
    landing_moment: float
    landing_arm: float
    landing_cg: float


@dataclass
class Moments:
    basic_empty_moment: float
    crew_moment: float
    side_facing_seat_moment: float
    passengers_1_and_2_moment: float
    passengers_3_and_4_moment: float
    belted_toilet_seat_moment: float
    forward_baggage_moment: float
    lh_aft_cabinet_moment: float
    aft_baggage_moment: float


@dataclass
class WeightAndBalance:
    weight: float
    arm: float
    moment: float

