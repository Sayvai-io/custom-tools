# Read Local CSV File
import os

import pandas as pd


class Excel:
    def __init__(self, path):
        self.path = path

    def read(self):
        if os.path.exists(self.path):
            return pd.read_excel(self.path)
        else:
            print("File not found")
            return None

    def write(self, data, sheet_name="Sheet1"):
        if os.path.exists(self.path):
            writer = pd.ExcelWriter(self.path, engine="xlsxwriter")
            data.to_excel(writer, sheet_name=sheet_name)
            writer.save()
            writer.close()
        else:
            print("File not found")
            return None

    def read_column(self, column_name):
        df = self.read()
        return df[column_name].tolist()
