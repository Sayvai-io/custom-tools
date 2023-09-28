import os.path
import datetime as dt
from typing import Dict
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from constants import SCOPES


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
            return "Error occured"

    def display_events(self, date, max_results: int = 10):
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
            return "Error occured"

    def create_event(self, event: Dict):
        try:
            self.get_service()
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            return "Event created"
        except HttpError as e:
            print(e)
            return "Error occured"

    def delete_event(self, event_id: str):
        """Deletes the event with the given event_id"""
        try:
            self.get_service()
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            return "Event deleted"
        except HttpError as e:
            print(e)
            return "Error occured"

    @staticmethod
    def parse_date(input_str):
        try:
            year, month, day, hour, minute = map(int, input_str.split(','))
            date = dt.datetime(year, month, day, hour, minute)
            return date
        except ValueError:
            return None

    @staticmethod
    def check_is_slot_available(start_time, end_time, booked_slots):
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
        input_pairs = date.split('/')
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])
        mail = input_pairs[2]
        clinic_open_time = 9
        clinic_close_time = 17

        current_datetime = dt.datetime.now()

        # Check if the provided date and time are in the past
        if start_time < current_datetime:
            return "The provided date and time are in the past."

        specific_date = start_time.date()  # Use the date from the input

        booked_slots = []

        for start, end, summary, descript, event_id in self.display_events(specific_date):
            booked_slots.append(start + ' ' + end)
            if summary == "day is not available for booking":
                start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
                end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

                # print(start_time_with_timezone, end_time_with_timezone)
                # print(start, end)

                if ((start < start_time_with_timezone < end and start < end_time_with_timezone < end) or
                        (start_time_with_timezone < end and end_time_with_timezone > start)):
                    # print(start, end)
                    return descript

        time_interval = start_time.isoformat() + '+05:30' + ' ' + end_time.isoformat() + '+05:30'

        start_time, end_time = time_interval.split(' ')
        start_time = dt.datetime.fromisoformat(start_time)
        end_time = dt.datetime.fromisoformat(end_time)

        if end_time <= start_time:
            return "End time should be greater than start time."

        duration = end_time - start_time
        if duration < dt.timedelta(minutes=15) or duration > dt.timedelta(hours=1):
            return "The slot should be between 15 minutes and 1 hour."

        if clinic_open_time <= start_time.hour < clinic_close_time and clinic_open_time <= end_time.hour < clinic_close_time:

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
                        {'email': 'sridhanush@sayvai.io'},
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
                {'email': 'sridhanush@sayvai.io'},
            ]
        }

        specific_date = start_time.date()  # Use the date from the input

        # booked_slots_block_day = []

        for start, end, summary, descript, event_id in self.display_events(specific_date):
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
            end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

            if ((((start < start_time_with_timezone < end and start < end_time_with_timezone < end) or
                  (start_time_with_timezone < end and end_time_with_timezone > start))) and
                    summary != "day is not available for booking"):

                # time = start.isoformat() + ' ' + end.isoformat()
                # booked_slots_block_day.append((time, event_id))
                self.delete_event(event_id)

                #TODO: send message to the user that the slot is deleted either via email or via whatsapp

        # print(booked_slots_block_day)
        return self.create_event(events)
