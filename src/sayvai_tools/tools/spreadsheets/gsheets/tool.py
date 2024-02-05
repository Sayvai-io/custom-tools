from sayvai_tools.utils.google.sheets import GSheets


class Sheets:
    name = "sheets"
    description = (
        "Useful for creating and updating sheets."
        "You can use sheets to generate reports."
        """Input: [["Name", "Age"], ["John", "20"], ["Jane", "19"]]"""
    )

    def __init__(self):
        self.gs = GSheets()

    @classmethod
    def create(cls) -> cls:
        return cls()

    def _run(self, values: list):
        self.gs.create_sheet()
        self.gs.update_values(values)
        return "Data has been exported to Google Sheets"

    async def _arun(self, date: str):
        raise NotImplementedError("Sheets async not implemented")
