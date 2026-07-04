from models.flight_model import BalanceData, FlightData, PassengerData, NoteData, CrewMember, Passenger, Airport
from datetime import datetime, time, date


def getFloat(prompt: str, minimum=0) -> float:
    while True:
        try:

            value = float(input(prompt).strip() or 0)
            
            if value < minimum:
                print(f"Value must be at least {minimum}")
                continue

            return value

        except ValueError:
            print("Invalid number! Please enter a valid weight.")


def getString(prompt: str) -> str:
    return input(prompt).strip()


def getInt(prompt: str, default=0) -> int:
    while True:
        try:
            value = input(prompt).strip()

            if value == "":
                return default

            return int(value)

        except ValueError:
            print("Invalid integer!")


def getDate(prompt: str, default = "") -> date:
    while True:
        try:
            text = input(prompt).strip()

            if text == "":
                return default

            value = datetime.strptime(
                text,
                "%d/%m/%Y"
            ).date()

            return value

        except ValueError:
            print("Invalid date format! Use DD/MM/YYYY")


def getTime(prompt: str, default = "") -> time:
    while True:
        try:
            text = input(prompt).strip()

            if text == "":
                return default

            value = datetime.strptime(
                text,
                "%H:%M"
            ).time()

            return value

        except ValueError:
            print("Invalid time format! Use HH:MM")


def getUserInput() -> BalanceData:

    print("\n\n - Balance Data:")
    
    return BalanceData(
        crew_weight=getFloat("\nCrew weight: ", 1),
        side_facing_seat_weight=getFloat("\nSide facing seat weight: ", 0),
        passengers_1_and_2_weight=getFloat("\nPassengers 1 and 2 weight: ", 0),
        passengers_3_and_4_weight=getFloat("\nPassengers 3 and 4 weight: ", 0),
        belted_toilet_seat_weight=getFloat("\nBelted toilet seat weight: ", 0),
        forward_baggage_compartment_weight=getFloat("\nForward baggage compartment weight: ", 0),
        lh_aft_cabinet_weight=getFloat("\nLH Aft cabinet weight: ", 0),
        aft_baggage_compartment_weight=getFloat("\nAft baggage compartment weight: ", 0),
        take_off_fuel_weight=getFloat("\nTake off fuel weight: ", 1),
        landing_fuel_weight=getFloat("\nLanding fuel weight: ", 1)
    )


def getFlightInformation() -> FlightData:

    print("\n\n\n - Flight Data:")

    return FlightData(
        log_book_page=getInt("\n    Enter the Log Book Page: ", ""),
        flight_date=getDate("\n    Enter the date (DD/MM/YYYY): "),
        prefix=getString("\n    Enter the aircraft prefix: "),
        model=getString("\n    Enter the aircraft model: "),
        operator=getString("\n    Enter the operator: "),
        origin=Airport(
            location=getString("\n    Enter the city of origin: "),
            icao=getString("\n    Enter the ICAO code of origin: ").upper(),
        ),
        destination=Airport(
            location=getString("\n    Enter the city of destination: "),
            icao=getString("\n    Enter the ICAO code of destination: ").upper(),
        ),
        take_off_time=getTime("\n    Take off time (HH:MM): "),
        landing_time=getTime("\n    Landing time (HH:MM): "),
        pilot=CrewMember(
            name=getString("\n    Enter the pilot: "),
            license_number=getString("\n    Enter the pilot license: "),
        ),
        copilot=CrewMember(
            name=getString("\n    Enter the copilot:"),
            license_number=getString("\n    Enter the copilot license: "),
        ),
    )
    

def getPassengersData() -> PassengerData:

    passenger_data = PassengerData(passengers=[])

    print("\n\n\n - Passengers:")

    while True:
        number_of_passengers = getInt("\n    Enter the number of passengers: ")

        if number_of_passengers <= 6:
            for i in range(number_of_passengers):
                name = getString(f"\n    Enter the name of passenger {i + 1}: ")
                document = getString(f"\n    Enter the document of passenger {i + 1}: ")
                passenger_data.passengers.append(Passenger(name=name, document=document))
            break
        else:
            print("\n Maximum capacity is 6 passengers!")

    return passenger_data


def checkNotesLength(notes: str) -> str:
    while True:
        if len(notes) <= 190:
            return notes
        else:
            print("\n Maximum characters limit (190) reached!")
            notes = getString("\n Enter the note again: ")


def getNotesData() -> NoteData:        
    print("\n\n\n - Notes:")
    
    return NoteData(
        atis=checkNotesLength(getString("\n    Enter the Atis: ")),
        rto=checkNotesLength(getString("\n    Enter the RTO: ")),
        clearance=checkNotesLength(getString("\n    Enter the clearance: ")),
    )