from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader  # Para carregar imagens
from pdfrw import PdfReader, PdfWriter, PageMerge
import os

__all__ = ["generatePDF"]

input_pdf_path = "BOARDING-FORM.pdf"
output_pdf_path = "BOARDING-FORM-PREENCHIDO.pdf"
temp_pdf_paths = ["temp_page1.pdf", "temp_page2.pdf", "temp_page3.pdf"]
image_path = "graph.png"


def generatePDF(data):
    for i in range(3):
        c = canvas.Canvas(temp_pdf_paths[i])
        c.setFont("Helvetica", 11)

        if i == 0:  # Primeira página
            positions = {
                "LogBookPage": (187, 700),
                "dateFlight": (186, 673),
                "prefix": (312, 673),
                "model": (425, 673),
                "operator": (186, 646),
                "cityOrigin": (186, 619),
                "ICAOOrigin": (425, 619),
                "cityDestination": (186, 592),
                "ICAODestination": (425, 592),
                "takeOffHour": (186, 565),
                "landingHour": (425, 565),
                "pilot": (186, 538),
                "pilotLicense": (186, 511),
                "copilot": (186, 484),
                "copilotLicense": (186, 457),
            }

            for key, pos in positions.items():
                c.drawString(pos[0], pos[1], data[key])

            y_pos = 333
            for passenger in data["passengers"]:
                c.drawString(125, y_pos, passenger["name"])
                c.drawString(430, y_pos, passenger["document"])
                y_pos -= 50

        elif i == 1:  # Segunda página
            balance_positions = {
                "bew": [(292, 730), (347, 730), (423, 730)],
                "crew": [(292, 714), (347, 714), (423, 714)],
                "sideFacingSeat": [(292, 698), (347, 698), (423, 698)],
                "passengers1And2": [(292, 682), (347, 682), (423, 682)],
                "passengers3And4": [(292, 664), (347, 664), (423, 664)],
                "beltedToiletSeat": [(292, 647), (347, 647), (423, 647)],
                "forwardBaggageCompartment": [(292, 631), (347, 631), (423, 631)],
                "lhAftCabinet": [(292, 614), (347, 614), (423, 614)],
                "aftBaggageCompartment": [(292, 598), (347, 598), (423, 598)],
                "maximumZeroFuel": [(347, 581)],
                "adjustedZeroFuel": [(292, 565), (347, 565), (423, 565)],
                "takeOffFuel": [(292, 549), (347, 549), (423, 549)],
                "landingFuel": [(292, 482), (350, 482), (423, 482)],
                "AirplaneCGAndWeightTakeoff": [(292, 515), (352, 515), (423, 515)],
                "AirplaneCGAndWeightLanding": [(292, 456), (352, 456), (423, 456)],
                "takeOffCG": [(352, 498)],
                "landingCG": [(352, 432)],
            }

            for key, positions in balance_positions.items():
                values = data["tableValues"].get(key, [])
                for pos, value in zip(positions, values):
                    c.drawString(pos[0], pos[1], f"{value:.2f}" if isinstance(value, float) else str(value))

            # Adiciona a imagem
            try:
                img = ImageReader(image_path)
                img_x, img_y = 140, 40
                img_width, img_height = 300, 375
                c.drawImage(img, img_x, img_y, width=img_width, height=img_height)
            except Exception as e:
                print(f"Erro ao carregar a imagem: {e}")

        elif i == 2:  # Terceira página
            positions = {
                "atis": (160, 737),
                "rto": (160, 687),
                "clearance": (160, 634),
            }

            for key, pos in positions.items():
                c.drawString(pos[0], pos[1], data["notes"].get(key, ""))

        c.save()  # Salva cada página antes de passar para a próxima

    # Carrega o PDF original
    original_pdf = PdfReader(input_pdf_path)

    # Mescla cada página temporária no PDF original
    for i in range(3):
        overlay = PdfReader(temp_pdf_paths[i]).pages[0]
        PageMerge(original_pdf.pages[i]).add(overlay).render()

    # Salva o novo PDF preenchido
    PdfWriter(output_pdf_path, trailer=original_pdf).write()

    # Remove os arquivos temporários se existirem
    for temp_file in temp_pdf_paths + [image_path]:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"✅ PDF preenchido gerado com sucesso: {output_pdf_path}")
