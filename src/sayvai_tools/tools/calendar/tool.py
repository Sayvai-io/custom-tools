import datetime

from langchain.tools.base import BaseTool

from sayvai_tools.utils.gcalendar import GCalendar


class Calendar():

    name = "calendar"
    description = (
            "You can ask calendar tool to create an event for you."
                    )

    def _run(self, date: str):
        cal = GCalendar()
        return cal.book_slots(date)

    async def _arun(self, date: str):

        raise NotImplementedError("Calendar async not implemented")