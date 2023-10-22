import pandas as pd
from sqlalchemy import create_engine, text

from sayvai_tools.utils.sheets import GSheets


class SQLSheet:
    name = "sqlsheet"
    description = (
        "Useful for exporting SQL query results to a spreadsheet."
        "You can use this to generate reports."
    )

    def __init__(self, uri: str, sheet_path: str = 'output.xlsx'):
        self.connection = create_engine(uri).connect()
        self.sheet_path = sheet_path

    def _run(self, query: str):
        df = pd.read_sql_query(text(query), self.connection)
        df.to_excel(self.sheet_path, index=False)
        return f'Data has been exported to {self.sheet_path}'

class SQLGSheet:
    name = "sqlgsheet"
    description = (
        "Useful for exporting SQL query results to a G-Sheets."
        "You can use this to generate reports."
    )

    def __init__(self, uri: str):
        self.gs = GSheets()

    def _run(self, query: str):
        df = pd.read_sql_query(text(query), self.connection)
        data_dict = df.to_dict('split')
        data = data_dict['data'][0]
        columns = data_dict['columns']
        result = [columns]  # Start with the header
        result.append(data)  # Add the data
        self.gs.create_sheet()
        self.gs.update_values(result)
        return 'Data has been exported to Google Sheets'