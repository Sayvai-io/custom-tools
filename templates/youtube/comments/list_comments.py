from sayvai_tools.tools.youtube.comment_threads import (
    ListCommentsTool, get_youtube_credentials)

# Get YouTube credentials
credentials = get_youtube_credentials()

# Instantiate the tool
tool = ListCommentsTool(credentials=credentials)

# Set the video ID for which you want to list comment_threads
video_id = "NP9nBOOfk7Q"

try:
    # Execute the tool to list comment_threads
    comments = tool.run(
        tool_input={
            "video_id": video_id
        }
    )
    print("Comments listed successfully:")
    for comment in comments:
        print(comment)
except Exception as e:
    print("Error occurred while listing comment_threads:", e)
