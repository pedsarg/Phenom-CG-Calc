from models.balance_pdf_model import BalanceRow
from models.flight_model import FlightData, PassengerData
from pdf.pdf_positions import FLIGHT_INFORMATION_POSITIONS, BALANCE_POSITIONS, NOTES_POSITIONS
from pdf.file_paths import CG_GRAPH_PATH, DEFAULT_PDF_PATH, OUTPUT_PDF_PATH, TEMP_PDF_PATHS
from datetime import date, time
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from textwrap import wrap


__all__ = ["generate_pdf"]


def draw_right_aligned(c, x, y, text):
    width = c.stringWidth(text, "Helvetica", 11)
    c.drawString(x - width, y, text)


def format_balance_value(value):

    if isinstance(value, float):
        return f"{value:.3f}"

    return str(value)


def get_nested_attr(obj, attr_path: str):

    attrs = attr_path.split('.')

    current = obj

    for attr in attrs:
        current = getattr(current, attr)

    return current


def removeTempFiles():

    for temp_file in TEMP_PDF_PATHS:

        if temp_file.exists():
            temp_file.unlink()

    if CG_GRAPH_PATH.exists():
        CG_GRAPH_PATH.unlink()


def draw_page_one(
    flight_data: FlightData,
    passenger_data: PassengerData,
    c: canvas.Canvas
):

    for field, pos in FLIGHT_INFORMATION_POSITIONS.items():

        value = get_nested_attr(flight_data, field)

        if isinstance(value, date):
            value = value.strftime("%d/%m/%Y")

        elif isinstance(value, time):
            value = value.strftime("%H:%M")

        c.drawString(
            pos[0],
            pos[1],
            str(value)
        )

    y_pos = 333

    for passenger in passenger_data.passengers:

        c.drawString(125, y_pos, passenger.name)

        c.drawString(430, y_pos, passenger.document)

        y_pos -= 50


def draw_page_two(balance_table_data, c):

    for key, positions in BALANCE_POSITIONS.items():

        value = getattr(balance_table_data, key)

        if isinstance(value, BalanceRow):
            values = [
                value.arm,
                value.weight,
                value.moment
            ]
        else:
            values = [value]

        for pos, item in zip(positions, values):
            draw_right_aligned(
                c,
                pos[0],
                pos[1],
                format_balance_value(item)
            )

    if CG_GRAPH_PATH.exists():
        c.drawImage(
            str(CG_GRAPH_PATH),
            140,
            40,
            width=300,
            height=375
        )


def break_text(text, max_chars=67):
    return wrap(
        text,
        width=max_chars,
        break_long_words=False,
        break_on_hyphens=False
    )


def draw_page_three(data, c):

    line_height = 14

    for key, pos in NOTES_POSITIONS.items():

        text = getattr(data, key)

        wrapped_text = break_text(text, 67)

        y = pos[1]

        for line in wrapped_text:

            c.drawString(
                pos[0],
                y,
                line
            )

            y -= line_height


def merge_pdf():

    template_pdf = PdfReader(str(DEFAULT_PDF_PATH))

    overlay_pages = [
        PdfReader(str(TEMP_PDF_PATHS[0])),
        PdfReader(str(TEMP_PDF_PATHS[1])),
        PdfReader(str(TEMP_PDF_PATHS[2])),
    ]

    writer = PdfWriter()

    for template_page, overlay_pdf in zip(
        template_pdf.pages,
        overlay_pages
    ):

        overlay_page = overlay_pdf.pages[0]

        template_page.merge_page(overlay_page)

        writer.add_page(template_page)

    with open(str(OUTPUT_PDF_PATH), "wb") as output_file:
        writer.write(output_file)



def generate_pdf(report):

    for i in range(3):

        c = canvas.Canvas(str(TEMP_PDF_PATHS[i]))

        c.setFont("Helvetica", 11)

        if i == 0:

            draw_page_one(
                report.flight_data,
                report.passengers_data,
                c
            )

        elif i == 1:

            draw_page_two(
                report.balance_table_data,
                c
            )

        elif i == 2:

            draw_page_three(
                report.notes_data,
                c
            )

        c.save()

    merge_pdf()

    removeTempFiles()

    return str(OUTPUT_PDF_PATH)