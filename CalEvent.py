from datetime import datetime
from datetime import date
from datetime import time

class CalEvent:

    day = None
    startTime = None
    endTime = None
    name = ''
    location = ''
    calendar_id = 'Primary'

    #def __init__(self):
    #    pass

    def __init__(self, inday=None, start=0, end=0, eventName='', calid='Primary', loc=''):
        dt = datetime.now()

        if isinstance(start, str):
            #assumes it's in iso format
            self.startTime = datetime.fromisoformat(start).time()
        else:
            self.startTime = start

        if isinstance(end, str):
            #assumes it's in iso format
            self.endTime = datetime.fromisoformat(end).time()
        else:
            self.endTime = end

        if isinstance(inday, str):
            #assumes it's in iso format
            self.day = date.fromisoformat(inday)
        else:
            self.day = inday

        self.name = eventName
        self.calendar_id = calid

    def getTimesHrs(self):
        start = self.startTime.hour + self.startTime.minute/60 + self.startTime.second/3600
        end = self.endTime.hour + self.endTime.minute/60 + self.endTime.second/3600
        return start,end

    #def __init__(self, start, end, eventName, calid, loc):
    #    startTime = start
    #    endTime = end
    #    name = eventName
    #    location = loc
    #    calendar_id = calid
