import os.path
import datetime as dt
from typing import Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from constants import SCOPES
from sayvai_tools.utils.mail import EmailSender

from engine import pool
from sqlalchemy import text

# Create a cursor
cursor = pool.connect()

ORGANIZER_EMAIL = 'sridhanush@sayvai.io'
CLINIC_OPEN_TIME = 9
CLINIC_CLOSE_TIME = 17
# time slot should be within 15 minutes and 1 hour
MINIMUM_TIME_SLOT = 15
MAXIMUM_TIME_SLOT = 60


class GCalendar:

    def __init__(self) -> None:
        """Initializes the GCalender class"""
        self.service = None
        self.creds = None
        self.calendar_id = "primary"
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            self.get_credentials()
        # if self.creds and self.creds.expired and self.creds.refresh_token:
        #     self.creds.refresh(Request())

    def get_credentials(self):
        """Gets the credentials for the user"""
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self.creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())

        return "Credentials obtained"

    def get_service(self):
        """Gets the service for the user"""
        try:
            self.service = build('calendar', 'v3', credentials=self.creds)
            return "Service obtained"
        except Exception as e:
            print(e)
            return "Error occurred"

    def display_events(self, date, max_results: int = 10):
        """
        Displays the events for the given date
        :param date: The date for which the events are to be displayed
        :param max_results: The maximum number of events to be displayed
        :return: creates a generator with values start time,end time,summary,description,event id of the events for the given date
        """
        try:
            self.get_service()
            now = dt.datetime.combine(date, dt.time.min).isoformat() + 'Z'
            end = dt.datetime.combine(date, dt.time.max).isoformat() + 'Z'
            event_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now, timeMax=end,
                                                      maxResults=max_results, singleEvents=True,
                                                      orderBy='startTime').execute()
            events = event_result.get('items', [])
            if not events:
                return "No upcoming events found."
            for event in events:
                event_id = event["id"]
                summary = event['summary']
                description = event['description']
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))

                # print(start, end)
                yield start, end, summary, description, event_id

        except Exception as e:
            print(e)
            return "Error occurred"

    def create_event(self, event: Dict):
        """
        Creates an event for the given event
        :param event: The event to be created
        :return: The event created
        """
        try:
            self.get_service()
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            # print(event)
            return "Event created"
        except HttpError as e:
            print(e)
            return "Error occurred"

    def delete_event(self, event_id: str):
        """
        Deletes the event with the given event_id
        :param event_id:
        :return:
        """
        try:
            self.get_service()
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            return "Event deleted"
        except HttpError as e:
            print(e)
            return "Error occured"

    @staticmethod
    def parse_date(input_str):
        """
        Parses the date from the input string
        :param input_str:
        :return:
        """
        try:
            year, month, day, hour, minute = map(int, input_str.split(','))
            date = dt.datetime(year, month, day, hour, minute)
            return date
        except ValueError:
            return None

    @staticmethod
    def check_is_slot_available(start_time, end_time, booked_slots):
        """
        Checks if the slot is available for the given date
        :param start_time:
        :param end_time:
        :param booked_slots:
        :return:
        """
        # Check if the time interval is between 9 AM and 5 PM

        for slot in booked_slots:
            slot_start_str, slot_end_str = slot.split(' ')
            slot_start = dt.datetime.fromisoformat(slot_start_str)
            slot_end = dt.datetime.fromisoformat(slot_end_str)

            # Check if the time interval overlaps with any booked slot
            if start_time < slot_end and end_time > slot_start:
                return False  # Slot is not available

        return True  # Slot is available

    def book_slots(self, date):
        """
        Books the slot for the given date
        checks if the provided time is in the past
        checks if the slot is already booked
        checks if the slot is within open and close time
        checks if the slot is between 15 minutes and 1 hour
        :param date:
        :return: appointment event creation
        """

        # splits the input string into start time, end time and email
        input_pairs = date.split('/')
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])
        mail = input_pairs[2]

        current_datetime = dt.datetime.now()

        # Check if the provided date and time are in the past
        if start_time < current_datetime:
            return "The provided date and time are in the past."

        specific_date = start_time.date()  # Use the date from the input

        booked_slots = []

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(specific_date):
            booked_slots.append(start + ' ' + end)
            if summary == "day is not available for booking":

                # formatting the start, end and start_time, end_time to compare
                start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
                end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

                # print(start_time_with_timezone, end_time_with_timezone)
                # print(start, end)
                # checks if the given time interval overlaps with the blocked day time interval
                if ((start < start_time_with_timezone < end and start < end_time_with_timezone < end) or
                        (start_time_with_timezone < end and end_time_with_timezone > start)):
                    # print(start, end)
                    return descript

        time_interval = start_time.isoformat() + '+05:30' + ' ' + end_time.isoformat() + '+05:30'

        start_time, end_time = time_interval.split(' ')
        start_time = dt.datetime.fromisoformat(start_time)
        end_time = dt.datetime.fromisoformat(end_time)

        # checks if the input time interval is valid
        if end_time <= start_time:
            return "End time should be greater than start time."

        # checks if the given time interval is between minimum and maximum time slot
        duration = end_time - start_time
        if duration < dt.timedelta(minutes=MINIMUM_TIME_SLOT) or duration > dt.timedelta(minutes=MAXIMUM_TIME_SLOT):
            return "The slot should be between 15 minutes and 1 hour."

        # checks if the given time interval is within the open and close time
        if CLINIC_OPEN_TIME <= start_time.hour < CLINIC_CLOSE_TIME and CLINIC_OPEN_TIME <= end_time.hour < CLINIC_CLOSE_TIME:
            # Check if the slot is available
            if self.check_is_slot_available(start_time, end_time, booked_slots):
                # Check if the slot is within 9 AM - 5 PM
                events = {
                    'summary': 'Sayvai IO',
                    'location': 'Coimbatore, Tamil Nadu, India',
                    'description': 'default description',
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
                        {'email': ORGANIZER_EMAIL},
                        {'email': mail}
                    ]
                }
                return self.create_event(events)
            else:
                return "The slot is already booked.", booked_slots

        else:
            return "The slot is not within 9 AM - 5 PM."

    # def update_event(self, date: str):
    #     self.get_service()
    #     now = dt.datetime.combine(date, dt.time.min).isoformat() + 'Z'
    #     event_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now,
    #                                               maxResults=20, singleEvents=True,
    #                                               orderBy='startTime').execute()
    #     events = event_result.get('items', [])
    #     print(events)

    def block_day(self, date: str):
        """
        Blocks the day for the given date and time
        cancels the appointments that are in the given time interval and send a mail to the user
        :param date:
        :return: block event creation
        """
        input_pairs = date.split('/')
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])

        events = {
            'summary': 'day is not available for booking',
            'description': f'the doctor is not available from {start_time} to {end_time}',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'IST',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'IST',
            },
            'attendees': [
                {'email': ORGANIZER_EMAIL},
            ]
        }

        specific_date = start_time.date()  # Use the date from the input

        # booked_slots_block_day = []

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(specific_date):
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
            end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

            # checks if there are any appointments in the given time interval of the block day and deletes the appointment
            if ((((start < start_time_with_timezone < end and start < end_time_with_timezone < end) or
                  (start_time_with_timezone < end and end_time_with_timezone > start))) and
                    summary != "day is not available for booking"):
                # time = start.isoformat() + ' ' + end.isoformat()
                # booked_slots_block_day.append((time, event_id))

                self.delete_event(event_id)
                event_id = event_id.split('_')[0]

                # TODO: send message to the user that the slot is deleted either via whatsapp

                # query the database to get the email id of the user using the event id
                query = cursor.execute(text(f"""SELECT email FROM patient_info WHERE event_id = '{event_id}';"""))
                email = query.fetchone()[0]

                # send mail to the user that the appointment is cancelled
                mail_class = EmailSender(organizer_email='sridhanush46@gmail.com',
                                         smtp_username="sridhanush46@gmail.com",
                                         smtp_password="oyos mbew oxju wpbg")

                mail_class.send_email(receiver_email=email,
                                      subject="cancelling the appointment",
                                      message=f"sorry for the inconvenience caused. the doctor is not available on the "
                                              f"given date:{specific_date}  and time from {start_time} to {end_time}."
                                              f" please book another slot.")

        # print(booked_slots_block_day)
        # creates the block dat event
        return self.create_event(events)
