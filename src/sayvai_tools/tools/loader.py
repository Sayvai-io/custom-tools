from typing import Any, List

from langchain.tools import BaseTool

from sayvai_tools.tools.date import GetDate
from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool,
                                                get_calendar_credentials)
from sayvai_tools.tools.google_calendar.available_slots import \
    AvailableSlotsTool
from sayvai_tools.tools.google_calendar.create_event import CreateEventTool
from sayvai_tools.tools.google_calendar.display_events import DisplayEventsTool
from sayvai_tools.tools.google_sheets import (AppendDataTool,
                                              CreateSpreadsheetTool,
                                              GetCellValuesTool,
                                              UpdateSpreadsheetTool,
                                              get_sheets_credentials)
from sayvai_tools.tools.pdfreader import (ReadPagesTool, ReadPageTool,
                                          ReadPDFTool)
from sayvai_tools.tools.retrive_details import RetrieveEmail, RetrievePhone
from sayvai_tools.tools.send_mail import SendMail
from sayvai_tools.tools.sql_database import Database
# from sayvai_tools.tools.vectordb import ChromaDB, PGVectorDB, PineconeDB
from sayvai_tools.tools.youtube import get_youtube_credentials
from sayvai_tools.tools.youtube.comment_threads import (InsertCommentTool,
                                                        ListCommentsTool)
from sayvai_tools.tools.youtube.comments import (ListCommentRepliesTool,
                                                 ReplyToCommentTool)
from sayvai_tools.tools.youtube.utils import get_youtube_credentials

all_tools = {
    "CreateEventTool": CreateEventTool,
    "DisplayEventsTool": DisplayEventsTool,
    "AvailableSlotsTool": AvailableSlotsTool,
    "GetDate": GetDate,
    "SendMail": SendMail,
    "ReadPagesTool": ReadPagesTool,
    "ReadPDFTool": ReadPDFTool,
    "ReadPageTool": ReadPageTool,
    "CreateSpreadsheetTool": CreateSpreadsheetTool,
    "AppendDataTool": AppendDataTool,
    "GetCellValuesTool": GetCellValuesTool,
    "UpdateSpreadsheetTool": UpdateSpreadsheetTool,
    "ListCommentsTool": ListCommentsTool,
    "InsertCommentTool": InsertCommentTool,
    "ListCommentRepliesTool": ListCommentRepliesTool,
    "ReplyToCommentTool": ReplyToCommentTool,
    "RetrieveEmail": RetrieveEmail,
    "RetrievePhone": RetrievePhone,
    "Database": Database,
}


def load_tools(tool: str, **kwargs) -> BaseTool:
    tool = all_tools[tool].create(**kwargs) if all_tools[tool] else Exception(f"Tool {user_tools} not found")  # type: ignore
    return tool
