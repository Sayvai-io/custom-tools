from sayvai_tools.tools.youtube import get_youtube_credentials
from sayvai_tools.tools.youtube.comments import ReplyToCommentTool

# Get YouTube credentials
credentials = get_youtube_credentials()

# Instantiate the tool
tool = ReplyToCommentTool(credentials=credentials)

# Set the parent comment ID and text of the reply
parent_comment_id = "UgyryEI8nLFv-aoLcup4AaABAg"
reply_text = "thanks!"

try:
    # Execute the tool to reply to the comment
    tool.run(
        tool_input={"parent_comment_id": parent_comment_id, "text": reply_text})
    print("Reply posted successfully.")
except Exception as e:
    print("Error occurred while posting reply:", e)
