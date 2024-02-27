"""PDF Reader Tool"""

from langchain.tools import BaseTool

from sayvai_tools.utils.pdfreader import read_page, read_pages, read_pdf


class ReadPDFTool(BaseTool):
    """Read PDF Tool"""

    func = read_pdf
    name = "ReadPDFTool"
    description = "Read a PDF and return the text."

    @classmethod
    def create(cls) -> "ReadPDFTool":
        return cls()
    
    def _run(self, file_path: str) -> str:
        return read_pdf(file_path)


class ReadPagesTool(BaseTool):
    """Read Pages Tool"""

    func = read_pages
    name = "ReadPagesTool"
    description = "Read a PDF and return the text."

    @classmethod
    def create(cls) -> "ReadPagesTool":
        return cls()

    def _run(self, file_path: str) -> list:
        return read_pages(file_path)


class ReadPageTool(BaseTool):
    """Read Page Tool"""

    func = read_page
    name = "ReadPageTool"
    description = "Read a PDF and return the text."

    @classmethod
    def create(cls) -> "ReadPageTool":
        return cls()

    def _run(self, file_path: str, page_number: int) -> str:
        return read_page(file_path, page_number)
