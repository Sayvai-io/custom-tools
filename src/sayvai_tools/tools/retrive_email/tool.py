from sayvai_tools.utils.gcalendar import GCalendar
import datetime as dt
from sqlalchemy import text


class RetrieveEmail:

    def __init__(self, pool, scope: str):
        self.pool = pool
        self.cursor = self.pool.connect()
        self.scope = scope
        self.cal = GCalendar(self.scope)

    name = "Retrieve Email"
    description = (
        "Retrieve Email from the calendar"
    )

    def _run(self, date: str):
        input_dates = date.split('/')
        start_time = self.cal.parse_date(input_dates[0])
        end_time = self.cal.parse_date(input_dates[1])

        specific_date = start_time.date()

        email_list = []

        for start, end, summary, descript, event_id in self.cal.display_events(specific_date):
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
            end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

            # checks if there are any appointments in the given time interval of the block day and deletes the appointment
            if ((((start < start_time_with_timezone < end and start < end_time_with_timezone < end) or
                  (start_time_with_timezone < end and end_time_with_timezone > start))) and
                    summary != "day is not available for booking"):
                event_id = event_id.split('_')[0]

                query = self.cursor.execute(text(f"""SELECT phone FROM patient_info WHERE event_id = '{event_id}';"""))
                email = query.fetchone()[0]
                email_list.append(email)

        return email_list

    def _arun(self):
        raise NotImplementedError("This method is not implemented yet")