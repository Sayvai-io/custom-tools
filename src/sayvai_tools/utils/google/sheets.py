"""Google Sheets API""" ""
import datetime
import json
import os

import gspread
from gspread import utils


class GSheets:
    """Google Sheets API""" ""

    def __init__(self) -> None:
        self.gc, _user = self.authenticate()
        self.credential_path = os.environ["GOOGLE_CREDENTIALS_PATH"]

    def get_credentials(self):
        with open(self.credential_path) as f:
            data = json.load(f)
        return data

    def authenticate(self):
        credentials = self.get_credentials()
        # Check Creditentials is valid
        if not credentials:
            raise Exception("Invalid Credentials")
        # Authorize API
        return gspread.oauth_from_dict(credentials)

    def get_date(self):
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def create_sheet(self):
        # # Authorize API
        self.sheet = self.gc.create(f"Records-Upto-{self.get_date()}")

    def update_values(self, values: list):
        if not self.sheet:
            self.create_sheet()
        worksheet = self.sheet.get_worksheet(0)
        start_cell = "A1"
        end_cell = utils.rowcol_to_a1(len(values), len(values[0]))

        # Combine the start and end cells to form the range
        range_to_update = f"{start_cell}:{end_cell}"

        # Update the range with the values
        worksheet.update(
            range_to_update, values=values, value_input_option="USER_ENTERED"
        )

    def get_values(self):
        # For now, we will only work with the first sheet
        worksheet = self.sheet.get_worksheet(0)
        values = worksheet.get_all_values()
        return values
