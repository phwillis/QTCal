# main.py
# Paul Hudson
# Tthe purpose of this file is to bring together everything and display a daily dashboard
# This requires calls to 3 different outside sources:
#   Weather
#   Google Calendar
#   Email (specifically one email/day)

## TODO:
##      Add Thread classes to query:
##          Weather
##          Events
##          Email
##      display images as mail
##      show message when calendar empty
##      show message when calendar is unreachable
##      show message when no mail
##      add icons for weather outlook

import sys
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from datetime import date, timedelta, datetime
# from PyQt5.QtCore import QDate, QTime, QDateTime, QTimer

from cal2 import Ui_MainWindow
#from GCalEventList import GCalEventList

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    event_list = [("Take out trash", QtCore.QTime(20,0)), ("Sleep", QtCore.QTime(22,30))]
    NEW_DAY = QtCore.QTime(0,0)
    MAIL_CHECK = QtCore.QTime(7,30)
    verticalSpacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)


    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.eventFont = QtGui.QFont()
        self.eventFont.setBold(False)
        self.eventFont.setItalic(False)
        self.eventFont.setWeight(3)
        self.eventFont.setPointSize(14)

        self._show_time(QtCore.QTime.currentTime())
        self._show_date()
        self._show_events()

        # creating a timer object
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self._on_second_timer)
        timer.start(1000)

    
    def _on_second_timer(self):
        current_time = QtCore.QTime.currentTime()
        self._show_time(current_time)
        if current_time == self.NEW_DAY:
            self._show_date()
            self._clear_events()
            self._show_events()
            self._show_weather()
        elif current_time == self.MAIL_CHECK:
            self._delete_old_mail()
            self._display_mail()


    def _show_date(self):
        today = QtCore.QDate.currentDate()
        dStr = today.toString('dddd, MMM d, yyyy')
        self.dateLabel.setText(dStr)


    def _display_mail(self):
        pass


    def _delete_old_mail(self):
        pass


    def _show_events(self):
        layout = QtWidgets.QVBoxLayout()

        for title, startTime in self.event_list:
            evLabel = QtWidgets.QLabel(title + ' - ' + startTime.toString('hh:mm'), self.mailView)
            evLabel.setFont(self.eventFont)
            layout.addWidget(evLabel)

        layout.addSpacerItem(self.verticalSpacer)
        self.taskView.setLayout(layout)


    def _clear_events(self):
        pass


    def _show_weather(self):
        pass


    def _show_time(self, t):
        # converting QTime object to string
        tStr = t.toString('hh:mm:ss')

        # showing it to the label
        self.clockLabel.setText(tStr)



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
