from sayvai_tools.tools.youtube import get_youtube_credentials
from sayvai_tools.tools.youtube.comments import ListCommentRepliesTool

# Get YouTube credentials
credentials = get_youtube_credentials()

# Instantiate the tool
tool = ListCommentRepliesTool(credentials=credentials)

# Set the parent comment ID
parent_comment_id = "UgyryEI8nLFv-aoLcup4AaABAg"

try:
    # Execute the tool to list replies to the parent comment
    replies = tool.run(
        tool_input={
            "parent_comment_id": parent_comment_id
        }
    )
    print("Replies to the comment:", replies)
except Exception as e:
    print("Error occurred while listing comment replies:", e)
