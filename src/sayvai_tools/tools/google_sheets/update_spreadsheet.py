from typing import List, Optional, Type
from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_sheets.base import GoogleSheetsBaseTool

class UpdateSpreadsheetSchema(BaseModel):
    """Input schema for UpdateSpreadsheetTool."""
    spreadsheet_id: str = Field(
        ...,
        description="ID of the spreadsheet to update."
    )
    range_: str = Field(
        ...,
        description="The range of cells to update. For example, 'Sheet1!A1:B2'."
    )
    values: List[List[str]] = Field(
        ...,
        description="New values to update in the specified range."
    )

class UpdateSpreadsheetTool(GoogleSheetsBaseTool):
    """Tool for updating cell values in a Google Sheets spreadsheet."""
    name: str = "update_spreadsheet"
    description: str = "Use this tool to update cell values in a specified range of a Google Sheets spreadsheet."
    args_schema: Type[UpdateSpreadsheetSchema] = UpdateSpreadsheetSchema

    @classmethod
    def create(cls) -> "UpdateSpreadsheetTool":
        return cls()

    def _update_spreadsheet(
        self,
        spreadsheet_id: str,
        range_: str,
        values: List[List[str]]
    ) -> None:
        """Update cell values in the specified range of the Google Sheets spreadsheet.

        Args:
            spreadsheet_id: ID of the spreadsheet to update.
            range_: The range of cells to update.
            values: New values to update in the specified range.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        body = {
            "values": values
        }
        try:
            self.api_resource.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_,
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self,
        spreadsheet_id: str,
        range_: str,
        values: List[List[str]],
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> None:
        try:
            self._update_spreadsheet(spreadsheet_id, range_, values)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
