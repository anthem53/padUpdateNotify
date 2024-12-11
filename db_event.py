import db
import log
from datetime import datetime


def isExistEvent(eventName):

    sql = "SELECT 1 FROM event WHERE name = '%s'" % (eventName)
    db.execute(sql)
    result = db.fetchall(i)

    return len(result) > 0

'''
Event(name, link ,startDate, endDate)
'''
def insertEvent(event):

    name = event[0]
    link = event[1]
    status = "1"
    startDate = event[2]
    endDate = event[3]
    updateDate= getTimeFormat(datetime.today())

    sql = "INSERT INTO event (name, link, status, start_date, end_date, update_date) values ('%s','%s','%s','%s','%s','%s')" % (name, link, status, startDate,endDate,updateDate)
    db.execute(sql)

'''
 단건 조회
'''
def selectEvent(name):
    sql = "SELECT * FROM event WHERE name = '%s'" % (name)
    db.execute(sql)
    result = db.fetchall()
    print(result) 
    return result   

'''
다건조회
'''
def selectEventList():
    sql = "SELECT * FROM event"
    db.execute(sql)
    result = db.fetchall()
    print(result) 
    return result   
'''
다건조회 Only name
'''
def selectEventNameList():
    sql = "SELECT * FROM event"
    db.execute(sql)
    executeResult = db.fetchall()
    result = []
    for elem in executeResult:
        result.append(elem[0])
    return result  

'''
오픈중인 이벤트?
'''
def isOpenEvent(name,startDate,endDate):
    sql = "SELECT 1 FROM event WHERE name = '%s' AND startDate >= '%s' AND endDate <='%s'" % (eventName,startDate, endDate)
    db.execute(sql)
    result = db.fetchall(i)

    return len(result) > 0
    

def updateEventStatus(name, status):
    
    sql = "UPDATE event SET status = '%s' WHERE name = '%s'" % (str(status), name)
    db.execute(sql)
    
def deleteEvent(name):
    sql = "DELETE FROM event WHERE name = '%s'" %(name)
    db.execute(sql)

def getTimeFormat(targetDatetime):
    return targetDatetime.strftime("%Y-%m-%d")



if __name__ == "__main__":
    db.init_db()
    
    #insertEvent(("test eventname3","www.naver.com","2024-10-11","2244-12-14"))
    
    #print(selectEventList(),sep='\n')
    
    print(selectEventNameList())

    
    db.close()
    print("test")