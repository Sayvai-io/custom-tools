from sayvai_tools.tools.youtube.comment_threads import InsertCommentTool, get_youtube_credentials

# Get YouTube credentials
credentials = get_youtube_credentials()

# Instantiate the tool
tool = InsertCommentTool(credentials=credentials)

# Set the video ID and text of the comment to be inserted
video_id = "NP9nBOOfk7Q"
comment_text = "nice video!"

try:
    # Execute the tool to insert the comment
    tool.run(
        tool_input={
            "video_id": video_id,
            "text": comment_text
        }
    )
    print("Comment inserted successfully.")
except Exception as e:
    print("Error occurred while inserting comment:", e)
