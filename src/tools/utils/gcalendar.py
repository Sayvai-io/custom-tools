import os.path
import datetime as dt
from typing import Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tools.utils.constants import SCOPES

class GCalender:
    
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
    
    def display_events(self, max_results : int = 10):
        try:
            self.get_service()
            now = dt.datetime.utcnow().isoformat() + 'Z'
            event_result = self.service.events().list(calendarId=self.calendar_id, timeMin=now,
                                                       maxResults=max_results, singleEvents=True,
                                                       orderBy='startTime').execute()
            events = event_result.get('items', [])
            if not events:
                return "No upcoming events found."
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
        except Exception as e:
            print(e)
            return "Error occured"
        
    def create_event(self, event : Dict):
        try:
            self.get_service()
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            return "Event created"
        except HttpError as e:
            print(e)
            return "Error occured"
        
            
    def delete_event(self, event_id : str):
        """Deletes the event with the given event_id"""
        try:
            self.get_service()
            self.service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
            return "Event deleted"
        except HttpError as e:
            print(e)
            return "Error occured"