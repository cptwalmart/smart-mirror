# calendar_events.py
from __future__ import print_function
import datetime
import os.path
import tzlocal
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, time


# Only read-only access to Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_today_events():
    creds = None
    #authenticate by either using saved token or get a new one via browser
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('config/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    #connect to calendar api
    service = build('calendar', 'v3', credentials=creds)

    #restricts the window of time to today
    local_tz = tzlocal.get_localzone()  # Get system time zone (e.g., America/Chicago)

    today = datetime.now(local_tz).date()
    start_of_day = datetime.combine(today, time.min).astimezone(local_tz)
    end_of_day = datetime.combine(today, time.max).astimezone(local_tz)

    time_min = start_of_day.isoformat()
    time_max = end_of_day.isoformat()

    all_events = []
    #fetch events (upto ten)

    calendar_list = service.calendarList().list().execute()
    for cal in calendar_list['items']:
        events_result = service.events().list(
            calendarId=cal['id'],
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        all_events.extend(events_result.get('items', []))

    #sort all_events into chronological time
    all_events.sort(key=lambda e: e['start'].get('dateTime', e['start'].get('date')))
    #pull each event start and name, format to be ##:## AM/PM, return string list for display
    if not all_events:
        return ["No events today."]
    
    formatted = []
    for event in all_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = (
            datetime.fromisoformat(start).strftime('%I:%M %p')
            if 'T' in start else start
        )
        formatted.append(f"{start_time} – {event['summary']}")
    for event in all_events:
        print(event['summary'], event['start'])
    
    return formatted

