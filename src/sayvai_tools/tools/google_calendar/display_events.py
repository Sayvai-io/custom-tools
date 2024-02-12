from datetime import datetime
from typing import List, Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from sayvai_tools.tools.google_calendar.base import GoogleCalendarBaseTool


class DisplayEventsSchema(BaseModel):
    """Input schema for DisplayEventsTool."""

    calendar_id: str = Field(
        ...,
        description="ID of the calendar to fetch events from.",
    )
    max_results: Optional[int] = Field(
        10,
        description="Maximum number of events to fetch. Default is 10.",
    )


class DisplayEventsTool(GoogleCalendarBaseTool):
    """Tool for displaying events from Google Calendar."""

    name: str = "display_calendar_events"
    description: str = (
        "Use this tool to display upcoming events from a specified calendar."
    )
    args_schema: Type[DisplayEventsSchema] = DisplayEventsSchema

    def _display_events(
        self,
        calendar_id: str,
        max_results: int = 10,
    ) -> List[dict]:
        """Fetch and display events from a specific calendar.

        Args:
            calendar_id: ID of the calendar to fetch events from.
            max_results: Maximum number of events to fetch.

        Returns:
            List of dictionaries representing events.
        """
        events_result = (
            self.api_resource.events()
            .list(
                calendarId=calendar_id,
                timeMin=datetime.utcnow().isoformat() + "Z",
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        return events

    def _run(
        self,
        calendar_id: str,
        max_results: int = 10,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[dict]:
        try:
            events = self._display_events(calendar_id, max_results)
            return events
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
