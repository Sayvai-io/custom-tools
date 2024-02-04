"""init for tools module."""

from typing import List

from sayvai_tools.tools.calendar import Calendar, CalendarSql
from sayvai_tools.tools.calendar_block import BlockCalendar
from sayvai_tools.tools.conversational_human import ConversationalHuman
from sayvai_tools.tools.date import GetDate
from sayvai_tools.tools.display_events import DisplayEvents
from sayvai_tools.tools.forms import FormTool
from sayvai_tools.tools.pdfreader import ReadPagesTool, ReadPageTool, ReadPdfTool
from sayvai_tools.tools.retrive_details import RetrieveEmail, RetrievePhone
from sayvai_tools.tools.send_mail import SendMail
from sayvai_tools.tools.spreadsheets import Sheets, SQLSheet
from sayvai_tools.tools.sql_database import Database
from sayvai_tools.tools.TTS import VoiceOutputRun
from sayvai_tools.tools.vectordb import ChromaDB, PGVectorDB, PineconeDB
from langchain.tools import __all__ as langchain_tools

__all__: List[str] = [
    "Calendar",
    "CalendarSql",
    "BlockCalendar",
    "ConversationalHuman",
    "GetDate",
    "DisplayEvents",
    "FormTool",
    "RetrieveEmail",
    "RetrievePhone",
    "SendMail",
    "SQLSheet",
    "Sheets",
    "Database",
    "VoiceOutputRun",
    "ChromaDB",
    "PGVectorDB",
    "PineconeDB",
    "ReadPagesTool",
    "ReadPDFTool",
    "ReadPageTool",
]


def get_all_tools() -> List[str]:
    return __all__


def get_tool(tool_name: str) -> str:
    if tool_name in __all__:
        return tool_name
    else:
        return "Tool not found"


def get_langchain_tools() -> List[str]:
    return langchain_tools
