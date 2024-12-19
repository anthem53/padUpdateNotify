import db
import log
from datetime import datetime


def isExistEvent(eventName):
    sql = "SELECT 1 FROM event WHERE name = '%s'"
    db.execute(sql,(eventName))
    result = db.fetchall()

    return len(result) > 0

'''
Event(name, link ,startDate, endDate, status)
'''
def insertEvent(event):

    name = event[0]
    link = event[1]
    status = event[4]
    startDate = event[2]
    endDate = event[3]
    updateDate= getTimeFormat(datetime.today())

    sql = "INSERT INTO event (name, link, status, start_date, end_date, update_date) values (%s,%s,%s,%s,%s,%s)" 
    
    db.execute(sql,(name, link, status, startDate,endDate,updateDate))
        

'''
 단건 조회
'''
def selectEvent(name):
    sql = "SELECT * FROM event WHERE name = %s" 
    db.execute(sql,(name))
    result = db.fetchall()
    return result   

'''
다건조회
'''
def selectEventList():
    sql = "SELECT * FROM event"
    db.execute(sql)
    result = db.fetchall()
    return result   
'''
다건조회 Only name
'''
def selectEventNameList():
    sql = "SELECT name FROM event"
    db.execute(sql)
    result = db.fetchall()
    return [elem[0] for elem in result]

'''
오픈중인 이벤트?
'''
def isOpenEvent(name,startDate,endDate):
    sql = "SELECT 1 FROM event WHERE name = '%s' AND startDate >= '%s' AND endDate <='%s'" % (name,startDate, endDate)
    db.execute(sql)
    result = db.fetchall()
    return len(result) > 0

'''
이벤트 status 수정
'''
def updateEventStatus(name, status):
    sql = "UPDATE event SET status = '%s' WHERE name = '%s'" % (str(status), name)
    db.execute(sql)
    
'''
이벤트 삭제
'''
def deleteEvent(name):
    sql = "DELETE FROM event WHERE name = '%s'" %(name)
    db.execute(sql)

def getTimeFormat(targetDatetime):
    return targetDatetime.strftime("%Y-%m-%d")



if __name__ == "__main__":
    db.init_db()
    
    #insertEvent(("test eventname3","www.naver.com","2024-10-11","2244-12-14"))
    
    #print(selectEventList(),sep='\n')
    
    insertEvent(("testname","https://www.naver.com",None,None,"0"))

    
    db.close()
    print("test")