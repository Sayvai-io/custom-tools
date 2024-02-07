import datetime as dt
import os
import os.path
import time
from datetime import timedelta
from typing import Dict, List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich import print as rprint

from sayvai_tools.utils.google.mail import EmailSender

# checking


class GCalendar:
    def __init__(self, scope: str, summary=None, email=None) -> None:
        """Initializes the GCalender class"""
        self.service = None
        self.creds = None
        self.SCOPE = scope
        self.calendar_id = "primary"
        self.organizer_email = email
        self.summary = summary
        self.token_path = os.environ["GTOKEN_PATH"]
        self.credential_path = os.environ["GOOGLE_CREDENTIALS_PATH"]
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPE
            )
        else:
            self.get_credentials()
        # if self.creds and self.creds.expired and self.creds.refresh_token:
        #     self.creds.refresh(Request())
        # os.remove('token.json')

    def get_credentials(self):
        """Gets the credentials for the user"""
        flow = InstalledAppFlow.from_client_secrets_file(
            self.credential_path, self.SCOPE
        )
        self.creds = flow.run_local_server(port=0)

        with open(self.token_path, "w") as token:
            token.write(self.creds.to_json())

        return "Credentials obtained"

    def get_service(self):
        """Gets the service for the user"""
        try:
            self.service = build("calendar", "v3", credentials=self.creds)
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
            now = dt.datetime.combine(date, dt.time.min).isoformat() + "Z"
            end = dt.datetime.combine(date, dt.time.max).isoformat() + "Z"
            event_result = (
                self.service.events()
                .list(
                    calendarId=self.calendar_id,
                    timeMin=now,
                    timeMax=end,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = event_result.get("items", [])
            if not events:
                return "No upcoming events found."
            for event in events:
                event_id = event["id"]
                summary = event["summary"]
                description = event["description"]
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))

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
            event = (
                self.service.events()
                .insert(calendarId=self.calendar_id, body=event)
                .execute()
            )
            # print(event)
            return "Event created", event["id"]
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
            self.service.events().delete(
                calendarId=self.calendar_id, eventId=event_id
            ).execute()
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
            year, month, day, hour, minute = map(int, input_str.split(","))
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
            slot_start_str, slot_end_str = slot.split(" ")
            slot_start = dt.datetime.fromisoformat(slot_start_str)
            slot_end = dt.datetime.fromisoformat(slot_end_str)

            # Check if the time interval overlaps with any booked slot
            if start_time < slot_end and end_time > slot_start:
                return False  # Slot is not available

        return True  # Slot is available

    def book_slots(
        self,
        input_str: str,
        MINIMUM_TIME_SLOT: int = 15,
        MAXIMUM_TIME_SLOT: int = 60,
        OPEN_TIME: int = 9,
        CLOSE_TIME: int = 17,
    ):
        """
        Books the slot for the given date
        checks if the provided time is in the past
        checks if the slot is already booked
        checks if the slot is within open and close time
        checks if the slot is between 15 minutes and 1 hour
        :param CLOSE_TIME:
        :param MAXIMUM_TIME_SLOT:
        :param OPEN_TIME:
        :param MINIMUM_TIME_SLOT:
        :param input_str:
        :return: appointment event creation
        """
        startt = time.time()

        # splits the input string into start time, end time and email
        input_pairs = input_str.split("/")
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])
        phone = input_pairs[2]
        name = input_pairs[3]

        current_datetime = dt.datetime.now()

        # Check if the provided date and time are in the past
        if start_time < current_datetime:
            return "The provided date and time are in the past."

        specific_date = start_time.date()  # Use the date from the input

        booked_slots = []

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(
            specific_date
        ):
            booked_slots.append(start + " " + end)
            if summary == "day is not available for booking":
                # formatting the start, end and start_time, end_time to compare
                start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
                end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
                start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
                end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

                # print(start_time_with_timezone, end_time_with_timezone)
                # print(start, end)
                # checks if the given time interval overlaps with the blocked day time interval
                if (
                    start < start_time_with_timezone < end
                    and start < end_time_with_timezone < end
                ) or (
                    start_time_with_timezone < end and end_time_with_timezone > start
                ):
                    # print(start, end)
                    return descript

        time_interval = (
            start_time.isoformat() + "+05:30" + " " + end_time.isoformat() + "+05:30"
        )

        start_time, end_time = time_interval.split(" ")
        start_time = dt.datetime.fromisoformat(start_time)
        end_time = dt.datetime.fromisoformat(end_time)

        # checks if the input time interval is valid
        if end_time <= start_time:
            return "End time should be greater than start time."

        # checks if the given time interval is between minimum and maximum time slot
        duration = end_time - start_time
        if duration < dt.timedelta(
            minutes=MINIMUM_TIME_SLOT
        ) or duration > dt.timedelta(minutes=MAXIMUM_TIME_SLOT):
            return "The slot should be between 15 minutes and 1 hour."

        # checks if the given time interval is within the open and close time
        if (
            OPEN_TIME <= start_time.hour < CLOSE_TIME
            and OPEN_TIME <= end_time.hour < CLOSE_TIME
        ):
            # Check if the slot is available
            if self.check_is_slot_available(start_time, end_time, booked_slots):
                self.summary = self.summary.replace("{name}", name).replace(
                    "{phone}", phone
                )
                events = {
                    "summary": self.summary,
                    "location": "Coimbatore, Tamil Nadu, India",
                    "description": "default description",
                    "start": {
                        "dateTime": start_time.isoformat(),
                        "timeZone": "IST",
                    },
                    "end": {
                        "dateTime": end_time.isoformat(),
                        "timeZone": "IST",
                    },
                    "recurrence": ["RRULE:FREQ=DAILY;COUNT=1"],
                    "attendees": [
                        {"email": self.organizer_email},
                    ],
                }
                endd = time.time()
                total = endd - startt
                rprint(f"[bold green] Time taken: {total} [/bold green]")
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

    def block_day(
        self,
        date: str,
        contacts: List[str],
        organizer: str,
        smtp_username: str,
        smtp_password: str,
    ):
        """
        Blocks the day for the given date and time
        cancels the appointments that are in the given time interval and send a mail to the user
        :param contacts:
        :param organizer:
        :param smtp_username:
        :param smtp_password:
        :param date:
        :return: block event creation
        organizer : Role [doctor, dentist, event holder]
        """
        input_pairs = date.split("/")
        start_time = self.parse_date(input_pairs[0])
        end_time = self.parse_date(input_pairs[1])

        events = {
            "summary": "day is not available for booking",
            "description": f"the doctor is not available from {start_time} to {end_time}",
            "start": {
                "dateTime": start_time.isoformat(),
                "timeZone": "IST",
            },
            "end": {
                "dateTime": end_time.isoformat(),
                "timeZone": "IST",
            },
            "attendees": [
                {"email": self.organizer_email},
            ],
        }

        specific_date = start_time.date()  # Use the date from the input

        # booked_slots_block_day = []

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(
            specific_date
        ):
            start = dt.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            end = dt.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S%z")
            start_time_with_timezone = start_time.replace(tzinfo=start.tzinfo)
            end_time_with_timezone = end_time.replace(tzinfo=end.tzinfo)

            # checks if there are any appointments in the given time interval of the block day and deletes the appointment
            if (
                (
                    (
                        start < start_time_with_timezone < end
                        and start < end_time_with_timezone < end
                    )
                    or (
                        start_time_with_timezone < end
                        and end_time_with_timezone > start
                    )
                )
            ) and summary != "day is not available for booking":
                # time = start.isoformat() + ' ' + end.isoformat()
                # booked_slots_block_day.append((time, event_id))

                self.delete_event(event_id)
                # event_id = event_id.split('_')[0]

                # TODO: send message to the user that the slot is deleted either via whatsapp

                # send mail to the user that the appointment is cancelled
                mail_class = EmailSender(
                    organizer_email=self.organizer_email,
                    smtp_username=smtp_username,
                    smtp_password=smtp_password,
                )
                for email in contacts:
                    mail_class.send_email(
                        receiver_email=email,
                        subject="cancelling the appointment",
                        message=f"sorry for the inconvenience caused. the {organizer} is not available on the "
                        f"given date:{specific_date}  and time from {start_time} to {end_time}."
                        f" please book another slot.",
                    )

        # print(booked_slots_block_day)
        # creates the block dat event
        return self.create_event(events)

    def free_slots(self, date):
        """
        Finds the free slots for the given date
        :param date:
        :return: list containing the free slots
        """

        input_pairs = date.split("/")
        working_start = self.parse_date(input_pairs[0])
        working_end = self.parse_date(input_pairs[1])

        specific_date = working_start.date()
        booked_slots = []

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(
            specific_date
        ):
            booked_slots.append(start + " " + end)

        working_start = working_start.isoformat()
        working_end = working_end.isoformat()

        working_start = dt.datetime.strptime(
            f"{working_start}+05:30", "%Y-%m-%dT%H:%M:%S%z"
        )
        working_end = dt.datetime.strptime(
            f"{working_end}+05:30", "%Y-%m-%dT%H:%M:%S%z"
        )
        booked_slots = []

        specific_date = working_start.date()

        # calls display_events function to get the booked slots for the given date
        for start, end, summary, descript, event_id in self.display_events(
            specific_date
        ):
            booked_slots.append(start + " " + end)

        booked_ranges = []
        for slot in booked_slots:
            start_str, end_str = slot.split()
            start_time = dt.datetime.fromisoformat(start_str)
            end_time = dt.datetime.fromisoformat(end_str)
            booked_ranges.append((start_time, end_time))

        # Initialize the list of available time slots
        available_slots = []

        # Initialize the current time as the start of the working hours
        current_time = working_start

        # Iterate through the working hours
        while current_time < working_end:
            # Find the next available time slot
            next_slot_start = current_time
            while current_time < working_end:
                overlapping = False
                for booked_range in booked_ranges:
                    if (
                        current_time < booked_range[1]
                        and current_time + timedelta(minutes=30) > booked_range[0]
                    ):
                        overlapping = True
                        break
                if overlapping:
                    break
                current_time += timedelta(minutes=30)
            next_slot_end = current_time

            if next_slot_start < next_slot_end:
                available_slots.append(
                    f"{next_slot_start.strftime('%H:%M')} - {next_slot_end.strftime('%H:%M')} free"
                )

            # Move to the next 30-minute slot
            current_time += timedelta(minutes=30)

        free = []
        # Print the available time slots
        for slot in available_slots:
            free.append(slot)

        return ("booked_slots:", booked_slots), ("free slots:", free)
