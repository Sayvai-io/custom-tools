from typing import Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.youtube.base import YouTubeCommentsBaseTool


class ListCommentsSchema(BaseModel):
    """Input schema for ListCommentsTool."""

    video_id: str = Field(
        ..., description="ID of the YouTube video to list comment_threads for."
    )


class ListCommentsTool(YouTubeCommentsBaseTool):
    """Tool for listing comment_threads on a YouTube video."""

    name: str = "list_comments"
    description: str = "Use this tool to list comment_threads on a YouTube video."
    args_schema: Type[ListCommentsSchema] = ListCommentsSchema

    @classmethod
    def create(cls) -> "ListCommentsTool":
        return cls()

    def _list_comments(
        self,
        video_id: str,
    ) -> dict:
        """List comment_threads on the specified YouTube video.

        Args:
            video_id: ID of the YouTube video to list comment_threads for.

        Returns:
            List of comment_threads on the video.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        try:
            response = (
                self.api_resource.commentThreads()
                .list(part="snippet", videoId=video_id, textFormat="plainText")
                .execute()
            )
            return response
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self, video_id: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        try:
            comments = self._list_comments(video_id)
            return comments
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
