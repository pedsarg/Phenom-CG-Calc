from dataclasses import dataclass

from models.balance_pdf_model import BalanceTableData
from models.aircraft_configuration_model import GraphLimits
from models.calculation_model import TableRow
from models.flight_model import FlightData, PassengerData, BalanceData, NoteData, CgResult


@dataclass
class WeightBalanceTable:
    rows: list[TableRow]


@dataclass
class FlightReportData:
    flight_data: FlightData = None
    passengers_data: PassengerData = None
    balance_data: BalanceData = None
    notes_data: NoteData = None
    table: WeightBalanceTable = None
    cg_result: CgResult = None
    graph_limits: GraphLimits = None
    balance_table_data: BalanceTableData = None