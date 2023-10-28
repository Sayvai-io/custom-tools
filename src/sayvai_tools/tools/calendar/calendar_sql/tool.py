from sayvai_tools.utils.gcalendar import GCalendar
from sqlalchemy import text


class CalendarSql:
    name = "calendar_sql"
    description = "You can ask calendar_sql tool to create an event for you."

    def __init__(self, pool, scope: str, email: str, summary: str):
        self.pool = pool
        self.cursor = self.pool.connect()
        self.scope = scope
        self.email = email
        self.summary = summary
        self.cal = GCalendar(self.scope, email=self.email, summary=self.summary)

    def _run(self, details: str):
        start_time, end_time, phone, name = details.split("/")
        start_time = self.cal.parse_date(start_time)
        end_time = self.cal.parse_date(end_time)

        specific_date = start_time.date()
        date_string = specific_date.strftime("%Y-%m-%d")

        query = self.cursor.execute(text(f"""SELECT phone_number FROM patient_info;"""))
        phone_number = query.fetchall()
        phone_number = [i[0] for i in phone_number]
        result = self.cal.book_slots(details)
        if len(result) == 2 and result[0] == "Event created":
            msg, event_id = result[0], result[1]
            if details.split("/")[2] not in phone_number:
                query = self.cursor.execute(
                    text(
                        f"""INSERT INTO patient_info (name, phone_number, start_time, end_time, event_id, appointment_date) VALUES ('{name}', '{phone}'
                                            , '{start_time}', '{end_time}','{event_id}','{date_string}');"""
                    )
                )
                # query.commit()
            else:
                query = self.cursor.execute(
                    text(
                        f"""UPDATE patient_info SET start_time = '{start_time}', end_time = '{end_time}', event_id = '{event_id}', appointment_date = '{date_string}' WHERE phone_number = '{phone}';"""
                    )
                )
                # query.commit()

            return msg
        else:
            return result

    async def _arun(self, date: str):
        raise NotImplementedError("Calendar async not implemented")
