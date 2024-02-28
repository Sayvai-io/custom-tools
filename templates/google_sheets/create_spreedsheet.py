from sayvai_tools.tools.google_sheets import (CreateSpreadsheetTool,
                                              get_sheets_credentials)

credentials = get_sheets_credentials()

tool = CreateSpreadsheetTool(credentials=credentials)

# Set the title for the new spreadsheet
title = "Test Spreadsheet"

try:
    # Execute the tool to create a new spreadsheet
    spreadsheet_id = tool.run(
        tool_input={
            "title": title
        }
    )
    print("New spreadsheet created with ID:", spreadsheet_id)
except Exception as e:
    print("Error occurred:", e)
