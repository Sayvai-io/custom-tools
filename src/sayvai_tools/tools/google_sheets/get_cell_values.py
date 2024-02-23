from typing import List, Optional, Type
from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_sheets.base import GoogleSheetsBaseTool


class GetCellValuesSchema(BaseModel):
    """Input schema for GetCellValuesTool."""

    spreadsheet_id: str = Field(
        ..., description="ID of the spreadsheet containing the cells to retrieve."
    )
    range_: str = Field(
        ...,
        description="The range of cells to retrieve values from. For example, 'Sheet1!A1:B2'.",
    )


class GetCellValuesTool(GoogleSheetsBaseTool):
    """Tool for retrieving cell values from a Google Sheets spreadsheet."""

    name: str = "get_cell_values"
    description: str = (
        "Use this tool to retrieve cell values from a specified range in a Google Sheets spreadsheet."
    )
    args_schema: Type[GetCellValuesSchema] = GetCellValuesSchema

    def _get_cell_values(self, spreadsheet_id: str, range_: str) -> List[List[str]]:
        """Retrieve cell values from the specified range in the Google Sheets spreadsheet.

        Args:
            spreadsheet_id: ID of the spreadsheet containing the cells to retrieve.
            range_: The range of cells to retrieve values from.

        Returns:
            List of lists containing cell values.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        try:
            result = (
                self.api_resource.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_)
                .execute()
            )
            values = result.get("values", [])
            return values
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self,
        spreadsheet_id: str,
        range_: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[List[str]]:
        try:
            cell_values = self._get_cell_values(spreadsheet_id, range_)
            return cell_values
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
