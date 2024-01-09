from sayvai_tools.utils.google.gcalendar import GCalendar


class Calendar:
    name = "calendar"
    description = "You can ask calendar tool to create an event for you."

    def __init__(self, scope: str, email: str, summary: str):
        self.scope = scope
        self.email = email
        self.summary = summary
        self.cal = GCalendar(scope=self.scope, email=self.email, summary=self.summary)

    @classmethod
    def create(cls , scope: str, email: str, summary: str) -> cls:
        return cls(scope, email, summary)

    def _run(self, date: str):
        return self.cal.book_slots(input_str=date)

    async def _arun(self, date: str):
        raise NotImplementedError("Calendar async not implemented")
