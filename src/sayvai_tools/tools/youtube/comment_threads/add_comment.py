from typing import Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.youtube.base import YouTubeCommentsBaseTool


class InsertCommentSchema(BaseModel):
    """Input schema for InsertCommentTool."""
    video_id: str = Field(
        ...,
        description="ID of the YouTube video to insert the comment to."
    )
    text: str = Field(
        ...,
        description="Text of the comment to be inserted."
    )


class InsertCommentTool(YouTubeCommentsBaseTool):
    """Tool for inserting a comment on a YouTube video."""
    name: str = "insert_comment"
    description: str = "Use this tool to insert a comment on a YouTube video."
    args_schema: Type[InsertCommentSchema] = InsertCommentSchema

    @classmethod
    def create(cls) -> "InsertCommentTool":
        return cls()

    def _insert_comment(
            self,
            video_id: str,
            text: str
    ) -> None:
        """Insert a comment on the specified YouTube video.

        Args:
            video_id: ID of the YouTube video to insert the comment to.
            text: Text of the comment to be inserted.

        Raises:
            HttpError: If an HTTP error occurs during the API call.
            Exception: If any other error occurs.
        """
        try:
            self.api_resource.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": text
                            }
                        },
                        "videoId": video_id,
                    }
                }
            ).execute()
        except HttpError as e:
            raise HttpError(f"An HTTP error occurred: {e}", e.resp)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
            self,
            video_id: str,
            text: str,
            run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> None:
        try:
            self._insert_comment(video_id, text)
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
