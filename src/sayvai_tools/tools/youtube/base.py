# youtube_comments/base.py

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

from langchain_core.pydantic_v1 import Field
from langchain_core.tools import BaseTool

from sayvai_tools.tools.youtube.utils import build_youtube_service

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource
else:
    try:
        from googleapiclient.discovery import Resource
    except ImportError as e:
        raise ImportError("Please install google-api-python-client") from e


class YouTubeCommentsBaseTool(BaseTool, ABC):
    """Base class for YouTube Comments tools."""

    api_resource: Resource = Field(default_factory=build_youtube_service)

    @classmethod
    def from_api_resource(cls, api_resource: Resource) -> "YouTubeCommentsBaseTool":
        """Create a tool from an API resource.

        Args:
            api_resource: The API resource to use.

        Returns:
            A tool.
        """
        return cls(service=api_resource)
