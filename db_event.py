import db
import log


def isExistEvent(eventName):

    sql = "SELECT 1 FROM event WHERE name=%s" % (eventName)
    db.execute(sql)
    result = db.fetchall(i)

    return len(result) > 0


