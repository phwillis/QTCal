from datetime import date
from datetime import timedelta
from GCalEventList import GCalEventList

class WeekEvents:

    service = None
    daylists = []
    datelist = []
    weekday_nums = []
    weekday_names = []
    wd_nameref = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    tds = [timedelta(days=i) for i in range(7)]

    def __init__(self,day = None):
        if not day:
            day = date.today()

        self.datelist = [day + td for td in self.tds]
        self.weekday_nums = [date.weekday(d) for d in self.datelist]
        self.weekday_names = [self.wd_nameref[n] for n in self.weekday_nums]

        for d in self.datelist:
            el = GCalEventList(self.service)
            el.updateEvents(1, indate=d)

            self.daylists.append(el)

            if not self.service:
                self.service = el.get_service()

    def update_to_tomorrow(self):
        td = self.tds[1]
        self.datelist = [td + d for d in self.datelist]
        self.weekday_nums = [date.weekday(d) for d in self.datelist]
        self.weekday_names = [self.wd_nameref[n] for n in self.weekday_nums]

        self.daylists = []

        for d in self.datelist:
            el = GCalEventList(self.service)
            el.updateEvents(1, indate=d)

            self.daylists.append(el)

            if not self.service:
                self.service = el.get_service()

    def change_date(self,day):
        self.datelist = [day + td for td in self.tds]
        self.weekday_nums = [date.weekday(d) for d in self.datelist]
        self.weekday_names = [self.wd_nameref[n] for n in self.weekday_nums]
        self.daylists = []

        for d in self.datelist:
            el = GCalEventList(self.service)
            el.updateEvents(1, indate=d)

            self.daylists.append(el)

            if not self.service:
                self.service = el.get_service()

    def getEvents(self):
        return self.daylists    # returns a list of GCalEventLists, one for each day
