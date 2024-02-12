from sayvai_tools.tools.google_sheets import UpdateSpreadsheetTool, get_sheets_credentials

# Get Google Sheets credentials
credentials = get_sheets_credentials()

# Instantiate the tool
tool = UpdateSpreadsheetTool(credentials=credentials)

# Set the spreadsheet ID, range of cells, and new values
spreadsheet_id = "your_spreadsheet_id"
range_ = "Sheet1!A1:B2"  # Example range, adjust as needed
new_values = [
    ["New Value 1", "New Value 2"],
    ["New Value 3", "New Value 4"]
]

try:
    # Execute the tool to update cell values
    tool.run(
        spreadsheet_id=spreadsheet_id,
        range_=range_,
        values=new_values
    )
    print("Cell values updated successfully.")
except Exception as e:
    print("Error occurred while updating cell values:", e)
