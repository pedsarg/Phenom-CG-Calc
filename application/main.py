import shutil
import webbrowser
from pathlib import Path

from change_default_values import changeDefaultValues
from cg_calculator import calculateAdjustedZeroFuel, calculateFuelMoment, calculateMoments, calculateWeightAndBalance, convertArmToCGPercent
from terminalUI import getFlightInformation, getPassengersData, getNotesData, getUserInput
from aircraft_repository import getAircraftConfiguration, getFuelArm

from models.aircraft_configuration_model import AircraftConfiguration
from models.balance_pdf_model import BalanceRow, BalanceTableData
from models.flight_model import BalanceData, CgResult, FlightData
from models.flight_report_model import FlightReportData, WeightBalanceTable
from models.calculation_model import TableRow

from pdf.graph_generator import generate_cg_graph
from pdf.pdfEditor import generate_pdf
from pdf.file_paths import DEFAULT_PDF_PATH, TEMP_DIR


def openPDF(filePath: Path):
	webbrowser.open(f"file://{filePath}")


def calculateFlightReport(config: AircraftConfiguration, flight_data: FlightData, balance_data: BalanceData) -> FlightReportData:

    moments = calculateMoments(balance_data, config.weight_values, config.arm_values)
    adjusted_zero_fuel_balance = calculateAdjustedZeroFuel(balance_data, config.weight_values, moments)
    
    take_off_fuel_arm = getFuelArm(balance_data.take_off_fuel_weight)
    take_off_fuel_moment = calculateFuelMoment(take_off_fuel_arm, balance_data.take_off_fuel_weight)
    weight_and_balance_take_off = calculateWeightAndBalance(adjusted_zero_fuel_balance, balance_data.take_off_fuel_weight, take_off_fuel_moment) 
    take_off_cg = convertArmToCGPercent(weight_and_balance_take_off.arm)

    landing_fuel_arm = getFuelArm(balance_data.landing_fuel_weight)
    landing_fuel_moment = calculateFuelMoment(landing_fuel_arm, balance_data.landing_fuel_weight)
    weight_and_balance_landing = calculateWeightAndBalance(adjusted_zero_fuel_balance, balance_data.landing_fuel_weight, landing_fuel_moment)
    landing_cg = convertArmToCGPercent(weight_and_balance_landing.arm)
    
    cg_result = CgResult(
        take_off_weight=weight_and_balance_take_off.weight,
        take_off_moment=weight_and_balance_take_off.moment,
        take_off_arm=weight_and_balance_take_off.arm,
        take_off_cg=take_off_cg,

        landing_weight=weight_and_balance_landing.weight,
        landing_moment=weight_and_balance_landing.moment,
        landing_arm=weight_and_balance_landing.arm,
        landing_cg=landing_cg
    )
    
    table = WeightBalanceTable(
        rows=[
            TableRow(
                name="Basic Empty Weight",
                arm=config.arm_values.basic_empty_arm,
                weight=config.weight_values.basic_empty_weight,
                moment=moments.basic_empty_moment
            ),

            TableRow(
                name="Crew",
                arm=config.arm_values.crew_arm,
                weight=balance_data.crew_weight,
                moment=moments.crew_moment
            ),

            TableRow(
                name="Takeoff Fuel",
                arm=take_off_fuel_arm,
                weight=balance_data.take_off_fuel_weight,
                moment=take_off_fuel_moment
            ),
        ]
    )

    balance_table_data = BalanceTableData(

        bew=BalanceRow(
            arm=config.arm_values.basic_empty_arm,
            weight=config.weight_values.basic_empty_weight,
            moment=moments.basic_empty_moment
        ),

        crew=BalanceRow(
            arm=config.arm_values.crew_arm,
            weight=balance_data.crew_weight,
            moment=moments.crew_moment
        ),

        side_facing_seat=BalanceRow(
            arm=config.arm_values.side_facing_seat_arm,
            weight=balance_data.side_facing_seat_weight,
            moment=moments.side_facing_seat_moment
        ),

        passengers_1_and_2=BalanceRow(
            arm=config.arm_values.passengers_1_and_2_arm,
            weight=balance_data.passengers_1_and_2_weight,
            moment=moments.passengers_1_and_2_moment
        ),

        passengers_3_and_4=BalanceRow(
            arm=config.arm_values.passengers_3_and_4_arm,
            weight=balance_data.passengers_3_and_4_weight,
            moment=moments.passengers_3_and_4_moment
        ),

        belted_toilet_seat=BalanceRow(
            arm=config.arm_values.belted_toilet_seat_arm,
            weight=balance_data.belted_toilet_seat_weight,
            moment=moments.belted_toilet_seat_moment
        ),

        forward_baggage_compartment=BalanceRow(
            arm=config.arm_values.forward_baggage_compartment_arm,
            weight=balance_data.forward_baggage_compartment_weight,
            moment=moments.forward_baggage_moment
        ),

        lh_aft_cabinet=BalanceRow(
            arm=config.arm_values.lh_aft_cabinet_arm,
            weight=balance_data.lh_aft_cabinet_weight,
            moment=moments.lh_aft_cabinet_moment
        ),

        aft_baggage_compartment=BalanceRow(
            arm=config.arm_values.aft_baggage_compartment_arm,
            weight=balance_data.aft_baggage_compartment_weight,
            moment=moments.aft_baggage_moment
        ),

        adjusted_zero_fuel=BalanceRow(
            arm=adjusted_zero_fuel_balance.arm,
            weight=adjusted_zero_fuel_balance.weight,
            moment=adjusted_zero_fuel_balance.moment
        ),

        take_off_fuel=BalanceRow(
            arm=take_off_fuel_arm,
            weight=balance_data.take_off_fuel_weight,
            moment=take_off_fuel_moment
        ),

        landing_fuel=BalanceRow(
            arm=landing_fuel_arm,
            weight=balance_data.landing_fuel_weight,
            moment=landing_fuel_moment
        ),

        airplane_weight_and_balance_takeoff=BalanceRow(
            arm=weight_and_balance_take_off.arm,
            weight=weight_and_balance_take_off.weight,
            moment=weight_and_balance_take_off.moment
        ),

        airplane_weight_and_balance_landing=BalanceRow(
            arm=weight_and_balance_landing.arm,
            weight=weight_and_balance_landing.weight,
            moment=weight_and_balance_landing.moment
        ),

        maximum_zero_fuel=config.weight_values.maximum_zero_fuel_weight,

        take_off_cg=take_off_cg,

        landing_cg=landing_cg
    )
    
    return FlightReportData(
        flight_data=flight_data,
        balance_data=balance_data,
        table=table,
        cg_result=cg_result,
        graph_limits=config.graph_limits,
        balance_table_data=balance_table_data
    )


def generateFlightReport():
    
    print("\n\n\nGenerate flight report!")
    
    config = getAircraftConfiguration()

    flight_data = getFlightInformation()

    passengers_data = getPassengersData()

    balance_data = getUserInput()

    notes_data = getNotesData()

    report = calculateFlightReport(
        config=config,
        flight_data=flight_data,
        balance_data=balance_data
    )

    report.notes_data = notes_data
    report.passengers_data = passengers_data

    generate_cg_graph(report)

    output_pdf_path = generate_pdf(report)

    print(
        f"\n\nFlight Report created successfully: "
        f"{output_pdf_path}"
    )

    openPDF(output_pdf_path)

    input("\nPress enter to continue!")


def openEmptyFlightReport():
    copied_file = (
        TEMP_DIR /
        f"{DEFAULT_PDF_PATH.name}"
    )

    shutil.copy(DEFAULT_PDF_PATH, copied_file)

    openPDF(copied_file)


def main():
    while 1:
        print("\n\n\n=======================================")
        print("       Phenom 100e CG Calculator       ")
        print("=======================================")
        print("\n 1 - Generate flight report\n 2 - Change the default values\n 3 - Open empty boarding form\n 4 - Exit")
        option = int(input("Enter an option: ")) 

        match option:
            case 1:
                generateFlightReport()
            case 2:
                changeDefaultValues()
            case 3:
                openEmptyFlightReport()
            case 4:
                print("Exiting...")
                return 0
            case _:
                print("Invalid option")


if __name__ == "__main__": 
    main()