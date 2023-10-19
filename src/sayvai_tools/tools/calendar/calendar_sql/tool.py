from sayvai_tools.utils.gcalendar import GCalendar
from sqlalchemy import text


class CalendarSql:
    name = "calendar_sql"
    description = (
        "You can ask calendar_sql tool to create an event for you."
    )

    def __init__(self, pool, scope: str):
        self.pool = pool
        self.cursor = self.pool.connect()
        self.scope = scope
        self.cal = GCalendar(self.scope)

    def _run(self, details: str):
        start_time, end_time, name, phone = details.split('/')
        start_time = self.cal.parse_date(start_time)
        end_time = self.cal.parse_date(end_time)

        query = self.cursor.execute(text(f"""SELECT phone_number FROM patient_info;"""))
        phone_number = query.fetchall()
        phone_number = [i[0] for i in phone_number]
        if details.split('/')[2] not in phone_number:
            query = self.cursor.execute(text(f"""INSERT INTO patient_info (name, phone_number, start_time, end_time) VALUES ('{name}', '{phone}'
                                        , '{start_time}', '{end_time}');"""))
            # query.commit()
        else:
            query = self.cursor.execute(text(f"""UPDATE patient_info SET start_time = '{start_time}', end_time = '{end_time}' WHERE phone_number = '{phone}';"""))
            # query.commit()

        return self.cal.book_slots(details)

    async def _arun(self, date: str):
        raise NotImplementedError("Calendar async not implemented")