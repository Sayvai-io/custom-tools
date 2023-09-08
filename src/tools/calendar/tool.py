from tools.utils.gcalendar import GCalender
import datetime
from langchain.tools.base import BaseTool

class Calendar(BaseTool):

    name = "calendar"
    description = (
            "You can ask calendar tool to create an event for you."
                    )
    
    def parse_date(self, input_str):
        try:
            year, month, day, hour, minute = map(int, input_str.split(','))
            dt = datetime.datetime(year, month, day, hour, minute)
            return dt
        except ValueError:
            return None

    def _run(self, date: str):
        cal = GCalender()
        # Parse the start and end times using the parse_date function
        input_pairs = date.split('/')
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])
        mail = input_pairs[2]

        if start_time and end_time:
            events = {
                'summary': 'Sayvai IO',
                'location': 'Coimbatore, Tamil Nadu, India',
                'description': 'Sayvai IO is a startup company',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'IST',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'IST',
                },
                'recurrence': [
                    'RRULE:FREQ=DAILY;COUNT=1'
                ],
                'attendees': [
                    {'email': 'sanjaypranav@sayvai.io'},
                    {'email': mail}
                ]
            }
            return cal.create_event(events)
        else:
            return None
        
    async def run_async(self, date: str):
        # Parse the start and end times using the parse_date function
        input_pairs = date.split('/')
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])
        mail = input_pairs[2]

        raise NotImplementedError("Calendar async not implemented")