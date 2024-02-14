from typing import Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.youtube.base import YouTubeCommentsBaseTool


class ReplyToCommentSchema(BaseModel):
    """Input schema for ReplyToCommentTool."""
    parent_comment_id: str = Field(
        ...,
        description="ID of the parent comment to reply to."
    )
    text: str = Field(
        ...,
        description="Text of the reply."
    )


class ReplyToCommentTool(YouTubeCommentsBaseTool):
    """Tool for replying to a comment on a YouTube video."""
    name: str = "reply_to_comment"
    description: str = "Use this tool to reply to a comment on a YouTube video."
    args_schema: Type[ReplyToCommentSchema] = ReplyToCommentSchema

    def _reply_to_comment(
            self,
            parent_comment_id: str,
            text: str
    ) -> None:
        """Reply to the specified parent comment.

        Args:
            parent_comment_id: ID of the parent comment to reply to.
            text: Text of the reply.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        try:
            self.api_resource.comments().insert(
                part="snippet",
                body={
                    "snippet": {
                        "parentId": parent_comment_id,
                        "textOriginal": text
                    }
                }
            ).execute()
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
            self,
            parent_comment_id: str,
            text: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> None:
        try:
            self._reply_to_comment(parent_comment_id, text)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
