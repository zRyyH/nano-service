import PyPDF2
from io import BytesIO


def extract_text_from_pdf(content: bytes) -> str:
    """
    Extracts text from a PDF file.

    Args:
        content: The binary content of the PDF file

    Returns:
        Extracted text as a string
    """
    pdf_text = ""

    # Read PDF file from binary content
    reader = PyPDF2.PdfReader(BytesIO(content))

    # Process each page
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

    return pdf_text
