from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

PDF_DIR = BASE_DIR / "storage" / "pdfs"

TEMP_DIR = BASE_DIR / "temp"


DEFAULT_PDF_PATH = (
    PDF_DIR / "BOARDING-FORM.pdf"
)

OUTPUT_PDF_PATH = (
    PDF_DIR / "BOARDING-FORM-COMPLETED.pdf"
)

TEMP_PDF_PATHS = [
    PDF_DIR / "tempPage1.pdf",
    PDF_DIR / "tempPage2.pdf",
    PDF_DIR / "tempPage3.pdf"
]

CG_GRAPH_PATH = (
    TEMP_DIR / "cg_graph.png"
)
