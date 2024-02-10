from sayvai_tools.tools.google_sheets import GetCellValuesTool, get_sheets_credentials

# Get Google Sheets credentials
credentials = get_sheets_credentials()

# Instantiate the tool
tool = GetCellValuesTool(credentials=credentials)

# Set the spreadsheet ID and range of cells
spreadsheet_id = "1cPbhoGg1ENX6dm_riyG4R4EFldcBvANjn9XgQQaX-DA"
range_ = "Sheet1!A1:B2"  # Example range, adjust as needed

try:
    # Execute the tool to get cell values
    cell_values = tool.run(
        tool_input={
            "spreadsheet_id": spreadsheet_id,
            "range_": range_
        }
    )
    print("Cell values retrieved successfully:")
    for row in cell_values:
        print(row)
except Exception as e:
    print("Error occurred while getting cell values:", e)
