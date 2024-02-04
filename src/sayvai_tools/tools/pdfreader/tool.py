"""PDF Reader Tool"""
from sayvai_tools.utils.pdfreader import (
    read_page,
    read_pdf,
    read_pages
)
from langchain.tools import BaseTool, StructuredTool, tool

class ReadPDFTool(BaseTool):
    """Read PDF Tool"""
    func = read_pdf
    name = "ReadPDFTool"
    description = "Read a PDF and return the text."

    def _run(self, file_path: str) -> str:
        return read_pdf(file_path)
    
class ReadPagesTool(BaseTool):
    """Read Pages Tool"""
    func = read_pages
    name = "ReadPagesTool"
    description = "Read a PDF and return the text."

    def _run(self, file_path: str) -> list:
        return read_pages(file_path)
    
class ReadPageTool(BaseTool):
    """Read Page Tool"""
    func = read_page
    name = "ReadPageTool"
    description = "Read a PDF and return the text."

    def _run(self, file_path: str, page_number: int) -> str:
        return read_page(file_path, page_number)