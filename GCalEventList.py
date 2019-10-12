import datetime
import pickle
import os.path
from tzlocal import get_localzone
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from CalEvent import CalEvent

class GCalEventList:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    evlist = []

    def __init__(self, inservice=None):
        if not inservice:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    self.creds = flow.run_local_server()
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('calendar', 'v3', credentials=self.creds)
        else:
            self.service = inservice


    def updateEvents(self, delta_days, year=None, month=None, day=None, indate=None, ignore=[]):
        if indate:
            startdate = indate
        elif not (year and month and day):
            startdate = datetime.date.today()
        else:
            startdate = datetime.date(year, month, day)

        tz = get_localzone()
        startTime = datetime.datetime(startdate.year, startdate.month, startdate.day, tzinfo=tz).isoformat()
        td = datetime.timedelta(days=delta_days)
        enddate = startdate+td
        endTime = datetime.datetime(enddate.year, enddate.month, enddate.day, tzinfo=tz).isoformat()

        events = []
        calendar_list = self.service.calendarList().list().execute()
        #print([c['summary'] for c in calendar_list['items']])
        for cal_list_entry in calendar_list['items'] :
            if cal_list_entry['summary'] in ignore:
                continue
            events_result = self.service.events().list(calendarId=cal_list_entry['id'], timeMin=startTime, timeMax=endTime, singleEvents=True, orderBy='startTime').execute()
            events += [(e,cal_list_entry['summary']) for e in events_result.get('items', [])]

        self.evlist = [CalEvent(e[0]['start'].get('date'), e[0]['start'].get('dateTime'), e[0]['end'].get('dateTime'), e[0]['summary'], e[1]) for e in events]
        for ce in self.evlist:
            if ce.startTime is None:
                ce.startTime = datetime.time(0,0)
                ce.endTime = datetime.time(11,59)

        if(len(self.evlist)>0):
            self.evlist.sort(key=lambda ce: ce.startTime)

    def get_list(self):
        return self.evlist

    def get_service(self):
        return self.service

    def find_next_for_calendar(self,id=None, summary=None):
        events_result = None
        if id is None and summary is None:
            print('You must supply either a calendar id or summary to search')
            return None
        elif not id is None:

            events_result = self.service.events().list(calendarId=id, timeMin=datetime.datetime.now(), maxResults=1, singleEvents=True, orderBy='startTime').execute()
            event = [(e,cal_list_entry['summary']) for e in events_result.get('items', [])][0]
        else:
            calendar_list = self.service.calendarList().list().execute()
            for ce in calendar_list['items']:
                if summary in ce['summary']:
                    events_result = self.service.events().list(calendarId=ce['id'], timeMin=datetime.datetime.now(), maxResults=1, singleEvents=True, orderBy='startTime').execute()
                    event = [(e,summary) for e in events_result.get('items', [])][0]
                    break
        if events_result is None:
            return None
