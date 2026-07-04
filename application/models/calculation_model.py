from dataclasses import dataclass


@dataclass
class TableRow:
    name: str
    arm: float | None
    weight: float | None
    moment: float | None


@dataclass
class CGResult:
    take_off_cg: float
    landing_cg: float