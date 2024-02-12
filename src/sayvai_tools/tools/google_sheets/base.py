"""Base class for Google Sheets tools."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

from sayvai_tools.tools.google_sheets.utils import build_sheets_service

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from googleapiclient.discovery import Resource
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from googleapiclient.discovery import Resource
    except ImportError as e:
        # Handle ImportError if googleapiclient is not installed
        raise ImportError("Please install google-api-python-client") from e


class GoogleSheetsBaseTool(BaseTool, ABC):
    """Base class for Google Sheets tools."""

    api_resource: Resource = Field(default_factory=build_sheets_service)

    @classmethod
    def from_api_resource(cls, api_resource: Resource) -> "GoogleSheetsBaseTool":
        """Create a tool from an API resource.

        Args:
            api_resource: The API resource to use.

        Returns:
            A tool.
        """
        return cls(service=api_resource)
