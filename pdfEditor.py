from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
import textwrap

__all__ = ["generatePDF"]

defaultPDFPath = "pdfs/BOARDING-FORM.pdf"
outputPDFPath = "pdfs/BOARDING-FORM-COMPLETED.pdf"
tempPDFPaths = ["pdfs/tempPage1.pdf", "pdfs/tempPage2.pdf", "pdfs/tempPage3.pdf"]
imagePath = "graph.png"


def getFlitghtInformationPositions():
    return {
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


def getBalancePositions():
    return {
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


def getNotesPositions():
    return {
                "atis": (160, 737),
                "rto": (160, 687),
                "clearance": (160, 634),
            }


def removeTempFiles():
    for temp_file in tempPDFPaths + [imagePath]:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def drawPageOne(data, c):
    flightInformationPositions = getFlitghtInformationPositions()

    for key, pos in flightInformationPositions.items():
        c.drawString(pos[0], pos[1], data["flightInformation"][key])

    y_pos = 333

    for passenger in data["passengers"]:
        c.drawString(125, y_pos, passenger["name"])
        c.drawString(430, y_pos, passenger["document"])
        y_pos -= 50


def drawPageTwo(data, c):
    balancePositions = getBalancePositions()
    for key, positions in balancePositions.items():
        values = data["tableValues"].get(key, [])
        
        for pos, value in zip(positions, values):
            c.drawString(pos[0], pos[1], f"{value:.2f}" if isinstance(value, float) else str(value))
    try:
        img = ImageReader(imagePath)
        img_x, img_y = 140, 40
        img_width, img_height = 300, 375
        c.drawImage(img, img_x, img_y, width=img_width, height=img_height)
    
    except Exception as e:
        raise ValueError("Error opening image")


def drawPageThree(data, c):
    notesPositions = getNotesPositions()
    maxWidth = 56
    lineHeight = 1
    
    for key, pos in notesPositions.items():
        text = data["notes"].get(key,"")
        wrappedText = textwrap.wrap(text, width=maxWidth)
        y = pos[1]
        
        for line in wrappedText:
            c.drawString(pos[0],y,line)
            y-= lineHeight


def mergePDF():
    originalPDF = PdfReader(defaultPDFPath)

    for i in range(3):
        overlay = PdfReader(tempPDFPaths[i]).pages[0]
        PageMerge(originalPDF.pages[i]).add(overlay).render()

    PdfWriter(outputPDFPath, trailer=originalPDF).write()


def generatePDF(data):
    for i in range(3):
        c = canvas.Canvas(tempPDFPaths[i])
        c.setFont("Helvetica", 11)

        if i == 0: 
            drawPageOne(data, c)
        elif i == 1:
            drawPageTwo(data, c)

        elif i == 2: 
            drawPageThree(data, c)

        c.save() 

    mergePDF()
    removeTempFiles()
    return outputPDFPath