from sayvai_tools.tools.google_sheets import AppendDataTool, get_sheets_credentials

credentials = get_sheets_credentials()

tool_append = AppendDataTool(credentials=credentials)
data_to_append = [
    ["Name", "Age", "Email"],
    ["John", "30", "john@example.com"],
    ["Alice", "25", "alice@example.com"]
]

try:
    # Execute the tool to append data to the spreadsheet
    tool_append.run(
        tool_input={
            "spreadsheet_id": "1cPbhoGg1ENX6dm_riyG4R4EFldcBvANjn9XgQQaX-DA",
            "data": data_to_append
        }
    )
    print("Data appended to the spreadsheet successfully.")
except Exception as e:
    print("Error occurred while appending data to the spreadsheet:", e)
