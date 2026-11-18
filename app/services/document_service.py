
from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError


def extract_text_from_pdf(content: bytes) -> str:
    """
    Extract text from a PDF document.
    """

    try:
        pdf_file = BytesIO(content)
        reader = PdfReader(pdf_file)

        extracted_text = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            extracted_text.append(page_text)

        return "\n".join(extracted_text).strip()

    except PdfReadError as exc:
        raise ValueError("Unable to read the PDF document.") from exc


def extract_text_from_txt(content: bytes) -> str:
    """
    Extract text from a TXT document.
    """

    try:
        return content.decode("utf-8-sig").strip()

    except UnicodeDecodeError as exc:
        raise ValueError("TXT file must use UTF-8 encoding.") from exc


def extract_document_text(
    content: bytes,
    file_extension: str
) -> str:
    """
    Extract text based on the uploaded file extension.
    """

    if file_extension == ".pdf":
        text = extract_text_from_pdf(content)

    elif file_extension == ".txt":
        text = extract_text_from_txt(content)

    else:
        raise ValueError("Unsupported document format.")

    if not text:
        raise ValueError(
            "The document does not contain extractable text."
        )

    return text
