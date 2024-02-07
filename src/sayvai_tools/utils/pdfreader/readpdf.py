# pip install pdfplumber
# --------------------------------

import fitz  # PyMuPDF

# Import things that are needed generically


def read_pdf(file_path: str) -> str:
    """Read the PDF and return the text."""
    doc = fitz.open(filename=file_path)  # open a document
    for page in doc:  # iterate the document pages
        text = page.get_text()  # get plain text encoded as UTF-8
        print(text)


def read_pages(file_path: str) -> list:
    """Read the PDF and return the text."""
    doc = fitz.open(filename=file_path)  # open a document
    pages = []
    for page in doc:  # iterate the document pages
        text = page.get_text()  # get plain text encoded as UTF-8
        pages.append(text)
    return pages


def read_page(file_path: str, page_number: int) -> str:
    """Read the PDF and return the text."""
    doc = fitz.open(filename=file_path)  # open a document
    page = doc.load_page(page_number)
    text = page.get_text()  # get plain text encoded as UTF-8
    return text


# --------------------------------
