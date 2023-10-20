import pandas as pd
from sqlalchemy import create_engine, text


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