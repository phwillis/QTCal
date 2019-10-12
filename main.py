import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from datetime import date, timedelta, datetime
# from PyQt5.QtCore import QDate, QTime, QDateTime, QTimer

from cal import Ui_MainWindow
from GCalEventList import GCalEventList
from CalEvent import CalEvent
from eventhandler import WeekEvents


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    event_lists = []
    scenes = []
    gview_w = 128
    gview_h = 338
    ampm = 0
    hr = 12
    minute = 0
    t_window = 60000

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.evhandler = WeekEvents()
        self.day = date.today()
        self.event_lists = self.evhandler.getEvents()
        for i in range(7):
            self.scenes.append(None)
        self.gviews = [self.calview1,self.calview2,self.calview3,self.calview4,self.calview5,self.calview6,self.calview7]
        self.dlabels = [self.daylabel1,self.daylabel2,self.daylabel3,self.daylabel4,self.daylabel5,self.daylabel6,self.daylabel7]

        t = datetime.now().time()
        self.hr = t.hour % 12
        if self.hr == 0:
            self.hr = 12
        self.minute = t.minute
        self.show_time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.inc_time)
        self.timer.start(self.t_window)

        for i in range(7):
            self.dlabels[i].setText(self.evhandler.weekday_names[i])
        self.draw_calendars()

    def update_calendars(self):
        self.updateEvents()
        for scene in self.scenes:
            scene.update()

    def inc_time(self):
        self.minute+=1
        if self.minute >= 60:
            self.minute = self.minute%60
            self.hr += 1
            if self.hr == 12:
                ampm^=1
            if self.hr > 12:
                self.hr = self.hr%12
            self.updateEvents(date.today())
        self.show_time()
        self.timer.start(self.t_window)

    def show_time(self):
        self.lcdHour.display(int(self.hr))
        self.lcdTens.display(int(self.minute/10))
        self.lcdones.display(int(self.minute)%10)

    def draw_calendars(self):
        pen = QtGui.QPen(QtCore.Qt.gray)
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        font = QtGui.QFont("Helvetica", 12, italic=True)
        for i in range(7):
            if self.scenes[i] is None:
                self.scenes[i] = QtWidgets.QGraphicsScene()
                self.scenes[i].setSceneRect(0,0,self.gview_w,self.gview_h)
                self.gviews[i].setScene(self.scenes[i])
            else:
                self.scenes.clear()

            ev_list = self.event_lists[i]
            ev_rs = []
            for calev in ev_list.get_list():
                startT, endT = calev.getTimesHrs()
                top_pos = self.gview_h*((startT-6.0)/15.0)
                bot_pos = self.gview_h*((endT-6.0)/15.0)
                r = QtCore.QRectF(2.0,top_pos,124.0,bot_pos-top_pos)
                ev_rs.append(self.scenes[i].addRect(r, pen, brush))

            if len(ev_rs) == 1:
                title = self.scenes[i].addText(ev_list.get_list()[0].name,font)
                tstr2 = self.scenes[i].addText(ev_list.get_list()[0].endTime.strftime("%-I:%M-"), font)
                tstr1 = self.scenes[i].addText(ev_list.get_list()[0].startTime.strftime("%-I:%M"), font)
                title.setPos(3, top_pos)
                tstr1.setPos(3, top_pos+13)
                tstr2.setPos(3, top_pos+26)
                continue

            for j in range(len(ev_rs)):
                items = ev_rs[j].collidingItems()
                if len(items) > 0:
                    r = ev_rs[j].rect()
                    r.setWidth(r.width()/2.0-1)
                    ev_rs[j].setRect(r)
                    for it in items:
                        r = it.rect()
                        r.setX(r.width()/2.0 + r.x() + 1)
                        #r.setWidth(r.width()/2.0 - 1)
                        it.setRect(r)

            for j in range(len(ev_rs)):
                title = self.scenes[i].addText(ev_list.get_list()[j].name,font)
                tstr1 = self.scenes[i].addText(ev_list.get_list()[j].startTime.strftime("%-I:%M-"), font)
                tstr2 = self.scenes[i].addText(ev_list.get_list()[j].endTime.strftime("%-I:%M"), font)
                title.setPos(ev_rs[j].rect().x(), ev_rs[j].rect().y())
                tstr1.setPos(ev_rs[j].rect().x(), ev_rs[j].rect().y()+13)
                tstr2.setPos(ev_rs[j].rect().x(), ev_rs[j].rect().y()+26)


    def updateEvents(self, day):
        self.day = day
        self.evhandler.change_date(day)
        self.event_lists = self.evhandler.getEvents()
        for i in range(7):
            dlabels[i].setText(self.evhandler.weekday_names[i])
        self.draw_calendars()



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
