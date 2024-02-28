from datetime import datetime, timedelta

from sayvai_tools.tools.google_calendar import (AvailableSlotsTool,
                                                CreateEventTool,
                                                DisplayEventsTool,
                                                get_calendar_credentials)

# Get Google Calendar credentials
credentials = get_calendar_credentials()

# Create an event
create_event_tool = CreateEventTool(credentials=credentials)
event = create_event_tool.run(
    {
        'summary': 'Meeting with John',
        'start_time': datetime.now() + timedelta(days=1),
        'end_time': datetime.now() + timedelta(days=1, hours=1),
    }
)

print("Event created:", event)
