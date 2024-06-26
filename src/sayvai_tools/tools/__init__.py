"""init for tools module."""

from typing import List

from langchain.tools import __all__ as langchain_tools

from sayvai_tools.tools.conversational_human import ConversationalHuman
from sayvai_tools.tools.date import GetDate
from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool,
                                                get_calendar_credentials)
from sayvai_tools.tools.google_sheets import (AppendDataTool,
                                              CreateSpreadsheetTool,
                                              GetCellValuesTool,
                                              UpdateSpreadsheetTool,
                                              get_sheets_credentials)
from sayvai_tools.tools.loader import load_tools
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
from sayvai_tools.tools.collect_data_from_user import CollectUserDataTool, create_data_model

__all__: List[str] = [
    "ConversationalHuman",
    "GetDate",
    "RetrieveEmail",
    "RetrievePhone",
    "SendMail",
    "Database",
    "ReadPagesTool",
    "ReadPDFTool",
    "ReadPageTool",
    "CreateEventTool",
    "DisplayEventsTool",
    "AvailableSlotsTool",
    "get_calendar_credentials",
    "CreateSpreadsheetTool",
    "get_sheets_credentials",
    "AppendDataTool",
    "GetCellValuesTool",
    "UpdateSpreadsheetTool",
    "get_youtube_credentials",
    "ListCommentsTool",
    "InsertCommentTool",
    "ListCommentRepliesTool",
    "ReplyToCommentTool",
    "load_tools",
    "CollectUserDataTool",
    "create_data_model"
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
