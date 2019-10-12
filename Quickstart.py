import datetime
import pickle
import os.path
from tzlocal import get_localzone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from CalEvent import CalEvent

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    #now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    nowdate = datetime.date.today()
    tz = get_localzone()
    startTime = datetime.datetime(nowdate.year, nowdate.month, nowdate.day, tzinfo=tz).isoformat()
    td = datetime.timedelta(days=7)
    enddate = nowdate+td
    endTime = datetime.datetime(enddate.year, enddate.month, enddate.day, tzinfo=tz).isoformat()
    
    events = []
    print('Getting events')
    calendar_list = service.calendarList().list().execute()
    for cal_list_entry in calendar_list['items']:
        events_result = service.events().list(calendarId=cal_list_entry['id'], timeMin=startTime, timeMax=endTime, singleEvents=True, orderBy='startTime').execute()
        events += [(e,cal_list_entry['summary']) for e in events_result.get('items', [])]
    
    event_list = [CalEvent(e[0]['start'].get('date'), e[0]['start'].get('dateTime'), e[0]['end'].get('dateTime'), e[0]['summary'], e[1]) for e in events]
    
    for event in event_list:
        print(event.calendar_id, ':', event.name, '   (', event.startTime,'-',event.endTime,')')

if __name__ == '__main__':
    main()
