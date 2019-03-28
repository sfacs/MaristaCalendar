import sqlite3

from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests
import datetime


class Event:
    eventId = -1
    date = None
    title = None
    description = None

    def __init__(self, eventId, date, title, description):
        self.eventId = eventId + date.strftime("%d-%m-%y")
        self.date = date
        self.title = title
        self.description = description

    def save(self):
        db = Sqlite("localendar.db")
        sql = ''' INSERT INTO events_event(eventId,date,title,description,done,hidden)
                      VALUES(?,?,?,?,?,?) '''
        cur = db.conn.cursor()
        try:
            cur.execute(sql, [self.eventId, self.date, self.title, self.description, False, False])
        except sqlite3.Error as e:
            print "Error id " + self.eventId
            print e
        return cur.lastrowid


class LocalendarParser:
    calendarId = None

    def __init__(self, calendarId):
        self.calendarId = calendarId

    def loadCurrentMonth(self):
        return self.loadMonth(datetime.date.today())

    def loadMonth(self, calendarMonth):
        url = "http://localendar.com/elsie?JSP=PublishedCalendar&mode=PUBLISH_PUBLIC&search_type=M1&start_date=" + calendarMonth.strftime(
            "%m/%d/%y") + "&calendar_id=" + self.calendarId
        print url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup

    def parseCurrentMonth(self):
        soup = self.loadCurrentMonth()
        eventsHtml = soup.find_all(class_="cal_" + self.calendarId)
        calendarEvents = []
        for eventHtml in eventsHtml:
            link = eventHtml.find("a")
            onclick = link['onclick']
            onclickArray = onclick.split(",")
            eventId = onclickArray[2]

            dt = onclickArray[4] + onclickArray[5]
            date = parse(dt.replace('"', ''))

            title = ""
            for string in link.find("span").strings:
                title += string + "\n"

            description = ""
            for string in eventHtml.find_all(class_="list-event-desc-usr")[0].strings:
                description += string + "\n"

            calendarEvent = Event(eventId, date, title, description)
            calendarEvents.append(calendarEvent)

        return calendarEvents


class Sqlite:
    conn = None
    dbFile = None

    def __init__(self, dbFile):
        self.dbFile = dbFile
        self.createConnection()

    def createConnection(self):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(self.dbFile, isolation_level=None)
        except sqlite3.Error as e:
            print(e)

    def close(self):
        self.conn.close()


localendarParser = LocalendarParser("422275")
events = localendarParser.parseCurrentMonth()
print len(events)
for event in events:
    print event.eventId
    event.save()

db = Sqlite("localendar.db")
db.close()
