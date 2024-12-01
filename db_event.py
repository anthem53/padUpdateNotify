import db
import log
from datetime import datetime


def isExistEvent(eventName):

    sql = "SELECT 1 FROM event WHERE name=%s" % (eventName)
    db.execute(sql)
    result = db.fetchall(i)

    return len(result) > 0

def insertEvent(event ,curDatetime):

    name = event[0]
    link = event[1]
    status = "1"
    startDate = event[2]
    endDate = event[3]
    updateDate= curDatetime

    sql = "INSERT INTO pad_event (event_name, event_link, status, start_date, end_date, update_date) values (%s,%s,%s,%s,%s,%s)" % (name, link, status, startDate,endDate,updateDate)
    db.execute(sql)



