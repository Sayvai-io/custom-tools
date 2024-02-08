from datetime import datetime, timedelta

from sayvai_tools.tools.google_calendar import \
    get_calendar_credentials  # Import build_calendar_service
from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool)

# Get Google Calendar credentials
credentials = get_calendar_credentials()

# Create an event
create_event_tool = CreateEventTool(credentials=credentials)
event = create_event_tool.run(
    tool_input={
        'calendar_id': 'primary',
        'summary': 'Meeting with John',
        'start_time': datetime.now() + timedelta(days=1),
        'end_time': datetime.now() + timedelta(days=1, hours=1),
    }
)

print("Event created:", event)
