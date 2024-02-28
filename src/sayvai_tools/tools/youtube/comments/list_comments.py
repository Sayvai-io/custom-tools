from typing import Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.youtube.base import YouTubeCommentsBaseTool


class ListCommentRepliesSchema(BaseModel):
    """Input schema for ListCommentRepliesTool."""

    parent_comment_id: str = Field(
        ..., description="ID of the parent comment to list replies for."
    )


class ListCommentRepliesTool(YouTubeCommentsBaseTool):
    """Tool for listing replies to a comment on a YouTube video."""

    name: str = "list_comment_replies"
    description: str = "Use this tool to list replies to a comment on a YouTube video."
    args_schema: Type[ListCommentRepliesSchema] = ListCommentRepliesSchema

    def _list_replies(
        self,
        parent_comment_id: str,
    ) -> dict:
        """List replies to the specified parent comment.

        Args:
            parent_comment_id: ID of the parent comment to list replies for.

        Returns:
            List of replies to the parent comment.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        try:
            response = (
                self.api_resource.comments()
                .list(
                    part="snippet", parentId=parent_comment_id, textFormat="plainText"
                )
                .execute()
            )
            return response
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self,
        parent_comment_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:
        try:
            replies = self._list_replies(parent_comment_id)
            return replies
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
