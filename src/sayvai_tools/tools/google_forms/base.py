"""Base class for Google Forms tools."""
from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

from sayvai_tools.tools.google_forms.utils import build_forms_service

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from googleapiclient.discovery import Resource
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from googleapiclient.discovery import Resource
    except ImportError:
        pass


class GoogleFormsBaseTool(BaseTool):
    """Base class for Google Forms tools."""

    api_resource: Resource = Field(default_factory=build_forms_service)

    @classmethod
    def from_api_resource(cls, api_resource: Resource) -> "GoogleFormsBaseTool":
        """Create a tool from an API resource.

        Args:
            api_resource: The API resource to use.

        Returns:
            A tool.
        """
        return cls(service=api_resource)
