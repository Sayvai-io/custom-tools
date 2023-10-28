from sayvai_tools.utils.gcalendar import GCalendar


class DisplayEvents:
    name = "Display Events"
    description = "Display events from the calendar"

    def __init__(self, scope: str):
        self.scope = scope
        self.cal = GCalendar(self.scope)

    def _run(self, date: str):
        date = self.cal.parse_date(date)
        specific_date = date.date()
        booked_slots = []
        for start, end, summary, descript, event_id in self.cal.display_events(
            specific_date
        ):
            booked_slots.append((start + " " + end, summary))

        return booked_slots

    def _arun(self):
        raise NotImplementedError("This method is not implemented yet")
