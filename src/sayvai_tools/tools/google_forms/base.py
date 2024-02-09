"""Base class for Google Forms tools."""
from __future__ import annotations

from typing import TYPE_CHECKING

from langchain_core.tools import BaseTool

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

    api_resource: Resource  # This should be defined in subclasses

    @classmethod
    def from_api_resource(cls, api_resource: Resource) -> "GoogleFormsBaseTool":
        """Create a tool from an API resource.

        Args:
            api_resource: The API resource to use.

        Returns:
            A tool.
        """
        return cls(service=api_resource)
