from sayvai_tools.utils.google.gcalendar import GCalendar


class BlockCalendar:
    name = "Block Day"
    description = "Block a day in the calendar"

    def __init__(
        self, organizer: str, smtp_username: str, smtp_password: str, scope: str
    ):
        self.organizer = organizer
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.scope = scope
        self.summary = None
        self.email = None
        self.cal = GCalendar(scope=self.scope, email=self.email, summary=self.summary)

    @classmethod
    def create(
        cls, organizer: str, smtp_username: str, smtp_password: str, scope: str
    ) -> "BlockCalendar":
        return cls(organizer, smtp_username, smtp_password, scope)

    def _run(self, date: str, contacts: list):
        self.cal.block_day(
            date=date,
            contacts=contacts,
            organizer=self.organizer,
            smtp_username=self.smtp_username,
            smtp_password=self.smtp_password,
        )
        return "Day is blocked"

    def _arun(self, date: str, contacts: list):
        raise NotImplementedError("This method is not implemented yet")
