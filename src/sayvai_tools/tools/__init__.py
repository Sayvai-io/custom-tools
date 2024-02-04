"""init for tools module."""

from typing import List
from sayvai_tools.tools.calendar import (
    Calendar,
    CalendarSql
)
from sayvai_tools.tools.calendar_block import BlockCalendar
from sayvai_tools.tools.conversational_human import ConversationalHuman
from sayvai_tools.tools.date import GetDate
from sayvai_tools.tools.display_events import DisplayEvents
from sayvai_tools.tools.forms import FormTool
from sayvai_tools.tools.retrive_details import (
    RetrieveEmail,
    RetrievePhone
)
from sayvai_tools.tools.send_mail import SendEmail
from sayvai_tools.tools.spreadsheets import (
    SQLSheet,
    Sheets
)
from sayvai_tools.tools.sql_database import Database
from sayvai_tools.tools.TTS import VoiceOutputRun 
from sayvai_tools.tools.vectordb import (
    ChromaDB,
    PGVectorDB,
    PineconeDB
)
from sayvai_tools.tools.pdfreader import (
    ReadPagesTool,
    ReadPdfTool,
    ReadPageTool
)



__all__ : List[str] = [
    "Calendar",
    "CalendarSql",
    "BlockCalendar",
    "ConversationalHuman",
    "GetDate",
    "DisplayEvents",
    "FormTool",
    "RetrieveEmail",
    "RetrievePhone",
    "SendEmail",
    "SQLSheet",
    "Sheets",
    "Database",
    "VoiceOutputRun",
    "ChromaDB",
    "PGVectorDB",
    "PineconeDB",
    "ReadPagesTool",
    "ReadPdfTool",
    "ReadPageTool"
]

def get_all_tools() -> List[Str]:
    return __all__

def get_tool(tool_name: Str) -> Str:
    if tool_name in __all__:
        return tool_name
    else:
        return "Tool not found"