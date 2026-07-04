import matplotlib.pyplot as plt

from pdf.file_paths import CG_GRAPH_PATH, TEMP_DIR
from models.flight_report_model import FlightReportData


def generate_cg_graph(report: FlightReportData):

    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 8))

    limits = report.graph_limits

    ax.plot(
        limits.limit_cg,
        limits.limit_weight,
        'k-'
    )

    ax.plot(
        limits.line_above_cg,
        limits.line_above_weight,
        'k-'
    )

    ax.plot(
        limits.side_line_cg,
        limits.side_line_weight,
        'k--'
    )

    ax.scatter(
        report.cg_result.take_off_cg,
        report.cg_result.take_off_weight,
        color='red',
        zorder=3,
        label="Take Off"
    )

    ax.scatter(
        report.cg_result.landing_cg,
        report.cg_result.landing_weight,
        color='blue',
        zorder=3,
        label="Landing"
    )

    ax.set_xlabel("CG POSITION - %MAC")
    ax.set_ylabel("Weight (kg)")
    ax.set_title("CG Position")
    ax.set_xlim(18, 40)
    ax.set_ylim(3000, 5000)

    ax.legend()

    ax.grid(True, linestyle="--", alpha=0.6)
    
    plt.savefig(CG_GRAPH_PATH, dpi=300, bbox_inches='tight')

    plt.close(fig)



