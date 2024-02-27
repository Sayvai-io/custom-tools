from typing import Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_sheets.base import GoogleSheetsBaseTool


class CreateSpreadsheetSchema(BaseModel):
    """Input schema for CreateSpreadsheetTool."""

    title: str = Field(..., description="Title of the new spreadsheet.")


class CreateSpreadsheetTool(GoogleSheetsBaseTool):
    """Tool for creating a new Google Sheets spreadsheet."""

    name: str = "create_spreadsheet"
    description: str = "Use this tool to create a new Google Sheets spreadsheet."
    args_schema: Type[CreateSpreadsheetSchema] = CreateSpreadsheetSchema

    @classmethod
    def create(cls) -> "CreateSpreadsheetTool":
        return cls()

    def _create_spreadsheet(self, title: str) -> str:
        """Create a new Google Sheets spreadsheet with the specified title.

        Args:
            title: Title of the new spreadsheet.

        Returns:
            str: ID of the newly created spreadsheet.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        spreadsheet = {"properties": {"title": title}}
        try:
            spreadsheet = (
                self.api_resource.spreadsheets()
                .create(body=spreadsheet, fields="spreadsheetId")
                .execute()
            )
            return spreadsheet["spreadsheetId"]
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self, title: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        try:
            spreadsheet_id = self._create_spreadsheet(title)
            return spreadsheet_id
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
