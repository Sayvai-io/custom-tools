from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_calendar.base import GoogleCalendarBaseTool


class AvailableSlotsSchema(BaseModel):
    """Input schema for AvailableSlotsTool."""

    calendar_id: str = Field(
        ...,
        description="ID of the calendar to check for available slots.",
    )
    start_time: datetime = Field(
        ...,
        description="Start time to search for available slots.",
    )
    end_time: datetime = Field(
        ...,
        description="End time to search for available slots.",
    )
    duration_minutes: int = Field(
        ...,
        description="Duration of the slots to search for, in minutes.",
    )


class AvailableSlotsTool(GoogleCalendarBaseTool):
    """Tool for finding available slots in a Google Calendar."""

    name: str = "find_available_slots"
    description: str = (
        "Use this tool to find available time slots in a specified Google Calendar."
    )
    args_schema: Type[AvailableSlotsSchema] = AvailableSlotsSchema

    def _find_available_slots(
        self,
        start_time: datetime,
        end_time: datetime,
        duration_minutes: int,
        calendar_id: str = "primary",
    ) -> List[Tuple[datetime, datetime]]:
        """Find available time slots in the specified Google Calendar.

        Args:
            calendar_id: ID of the calendar to check for available slots.
            start_time: Start time to search for available slots.
            end_time: End time to search for available slots.
            duration_minutes: Duration of the slots to search for, in minutes.

        Returns:
            List of tuples representing available time slots, each tuple containing
            the start and end times of a slot.
        """
        busy_events = self._get_busy_events(calendar_id, start_time, end_time)

        available_slots = []
        current_time = start_time.replace(tzinfo=timezone.utc)
        end_time_utc = end_time.replace(tzinfo=timezone.utc)
        while current_time < end_time_utc:
            slot_end_time = current_time + timedelta(minutes=duration_minutes)
            slot_end_time = slot_end_time.replace(tzinfo=timezone.utc)
            if all(
                event_end <= current_time or event_start >= slot_end_time
                for event_start, event_end in busy_events
            ):
                available_slots.append((current_time, slot_end_time))
            current_time += timedelta(minutes=duration_minutes)

        return available_slots

    def _get_busy_events(
        self,
        calendar_id: str,
        start_time: datetime,
        end_time: datetime,
    ) -> List[Tuple[datetime, datetime]]:
        """Get busy events from the specified Google Calendar.

        Args:
            calendar_id: ID of the calendar to check for busy events.
            start_time: Start time to check for busy events.
            end_time: End time to check for busy events.

        Returns:
            List of tuples representing busy events, each tuple containing
            the start and end times of an event.
        """
        events_result = (
            self.api_resource.events()
            .list(
                calendarId=calendar_id,
                timeMin=(start_time.astimezone(timezone.utc)).isoformat(),
                timeMax=(end_time.astimezone(timezone.utc)).isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        busy_events = []
        for event in events_result.get("items", []):
            start_time = datetime.fromisoformat(event["start"].get("dateTime"))
            end_time = datetime.fromisoformat(event["end"].get("dateTime"))
            busy_events.append((start_time, end_time))
        print(busy_events)
        return busy_events

    def _run(
        self,
        calendar_id: str,
        start_time: datetime,
        end_time: datetime,
        duration_minutes: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[Tuple[datetime, datetime]]:
        try:
            available_slots = self._find_available_slots(
                calendar_id, start_time, end_time, duration_minutes
            )
            return available_slots
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
