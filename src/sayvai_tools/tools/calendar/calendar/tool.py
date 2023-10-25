from sayvai_tools.utils.gcalendar import GCalendar


class Calendar:
    name = "calendar"
    description = (
        "You can ask calendar tool to create an event for you."
    )

    def __init__(self, scope: str, email: str):
        self.scope = scope
        self.email = email
        self.cal = GCalendar(self.scope, self.email)

    def _run(self, date: str):
        return self.cal.book_slots(date)

    async def _arun(self, date: str):
        raise NotImplementedError("Calendar async not implemented")
