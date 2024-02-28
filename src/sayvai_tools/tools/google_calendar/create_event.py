from datetime import datetime, timedelta
from typing import List, Optional, Type

from googleapiclient.errors import HttpError
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_calendar.base import GoogleCalendarBaseTool


class CreateEventSchema(BaseModel):
    """Input schema for CreateEventTool."""

    calendar_id: str = "primary"
    summary: str = Field(
        ...,
        description="Summary or title of the event.",
    )
    start_time: datetime = Field(
        ...,
        description="Start time of the event.",
    )
    end_time: datetime = Field(
        ...,
        description="End time of the event.",
    )
    description: Optional[str] = Field(
        None,
        description="Description or details of the event.",
    )
    location: Optional[str] = Field(
        None,
        description="Location of the event.",
    )
    attendees: Optional[List[str]] = Field(
        None,
        description="List of email addresses of attendees.",
    )


class CreateEventTool(GoogleCalendarBaseTool):
    """Tool for creating an event in Google Calendar."""

    name: str = "create_calendar_event"
    description: str = (
        "Use this tool to create an event in a specified Google Calendar."
    )
    args_schema: Type[CreateEventSchema] = CreateEventSchema

    @classmethod
    def create(cls) -> "CreateEventTool":
        return cls()

    def _create_event(
        self,
        calendar_id: str,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None,
    ) -> dict:
        """Create an event in the specified Google Calendar.

        Args:
            calendar_id: ID of the calendar to create the event in.
            summary: Summary or title of the event.
            start_time: Start time of the event.
            end_time: End time of the event.
            description: Description or details of the event.
            location: Location of the event.
            attendees: List of email addresses of attendees.

        Returns:
            Dictionary representing the created event.
        """
        event = {
            "summary": summary,            
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
        }
        if description:
            event["description"] = description
        if location:
            event["location"] = location
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            created_event = (
                self.api_resource.events()
                .insert(calendarId=calendar_id, body=event)
                .execute()
            )
            return created_event
        except HttpError as e:
            if e.resp.status == 409:
                raise HttpError(f"Event scheduling conflict: {e}", e.resp)
            else:
                raise Exception(f"An error occurred: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs,
    ) -> dict:
        try:
           created_event = self._create_event(
                calendar_id = kwargs.get("calendar_id", "primary"),
                summary = kwargs.get("summary","meeting"),
                start_time= kwargs.get("start_time",datetime.now()),
                end_time= kwargs.get("end_time",datetime.now()+timedelta(hours=1)),
                description =kwargs.get("description",None),
                location=kwargs.get("location",None),
                attendees=kwargs.get("attendees",None),
            )
            return created_event
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
