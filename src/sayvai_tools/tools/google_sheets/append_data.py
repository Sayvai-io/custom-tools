from typing import List, Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_sheets.base import GoogleSheetsBaseTool


class AppendDataSchema(BaseModel):
    """Input schema for AppendDataTool."""

    spreadsheet_id: str = Field(
        ..., description="ID of the spreadsheet to append data to."
    )
    data: List[List[str]] = Field(..., description="Data to append to the spreadsheet.")
    sheet_name: Optional[str] = Field(
        None,
        description="Name of the sheet within the spreadsheet. If not provided, data will be appended to the first sheet.",
    )


class AppendDataTool(GoogleSheetsBaseTool):
    """Tool for appending data to a Google Sheets spreadsheet."""

    name: str = "append_data_to_sheet"
    description: str = (
        "Use this tool to append data to a specified sheet in a Google Sheets spreadsheet."
    )
    args_schema: Type[AppendDataSchema] = AppendDataSchema

    def _append_data(
        self,
        spreadsheet_id: str,
        data: List[List[str]],
        sheet_name: Optional[str] = None,
    ) -> None:
        """Append data to the specified sheet in the Google Sheets spreadsheet.

        Args:
            spreadsheet_id: ID of the spreadsheet to append data to.
            data: Data to append to the spreadsheet.
            sheet_name: Name of the sheet within the spreadsheet. If not provided, data will be appended to the first sheet.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        range_ = sheet_name if sheet_name else "Sheet1"
        body = {"values": data}
        try:
            self.api_resource.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_,
                valueInputOption="USER_ENTERED",
                body=body,
            ).execute()
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self,
        spreadsheet_id: str,
        data: List[List[str]],
        sheet_name: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> None:
        try:
            self._append_data(spreadsheet_id, data, sheet_name)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
