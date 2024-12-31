import db
import log
from datetime import datetime

def init():
    db.init_db(getConnName())
    
def close ():
    db.close(getConnName())

def isExistEvent(eventName):
    sql = "SELECT 1 FROM event WHERE name = '%s'"
    db.execute(getConnName(),sql,(eventName))
    result = db.fetchall(getConnName())

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
    log.info("Insert event : " + name)
    
    sql = "INSERT INTO event (name, link, status, start_date, end_date, update_date) values (%s,%s,%s,%s,%s,%s)" 
    
    db.execute(getConnName(),sql,(name, link, status, startDate,endDate,updateDate))
        
'''
 단건 조회
'''
def selectEvent(name):
    sql = "SELECT * FROM event WHERE name = %s" 
    db.execute(getConnName(),sql,(name))
    result = db.fetchall(getConnName())
    return result   

'''
다건조회
'''
def selectEventList():
    sql = "SELECT * FROM event"
    db.execute(getConnName(),sql)
    result = db.fetchall(getConnName())
    return result   
'''
다건조회 Only name
'''
def selectEventNameList():
    sql = "SELECT name FROM event"
    db.execute(getConnName(),sql)
    result = db.fetchall(getConnName())
    return [elem[0] for elem in result]

#다건 조회 with Map
def selectEventNameDateList():
    sql = "SELECT name,update_date FROM event"
    db.execute(getConnName(),sql)
    result = db.fetchall(getConnName())
    resultMap = dict()
    for elem in result:
        resultMap[elem[0]] = elem[1].strftime("%Y-%m-%d")
    return resultMap

'''
오픈중인 이벤트?
'''
def isOpenEvent(name,startDate,endDate):
    sql = "SELECT 1 FROM event WHERE name = '%s' AND startDate >= '%s' AND endDate <='%s'" % (name,startDate, endDate)
    db.execute(getConnName(),sql)
    result = db.fetchall(getConnName())
    return len(result) > 0

def updateEventDate(name, endDate,updateDate):
    sql = "UPDATE event SET  end_date = %s, update_date = %s WHERE name = %s"
    db.execute(getConnName(),sql,(endDate,updateDate,name))
'''
이벤트 status 수정
'''
def updateEventStatus(name, status):
    sql = "UPDATE event SET status = '%s' WHERE name = '%s'" % (str(status), name)
    db.execute(getConnName(),sql)
    
'''
이벤트 삭제
'''
def deleteEvent(name):
    log.info("delete event [%s]" % (name))
    sql = "DELETE FROM event WHERE name = '%s'" %(name)
    db.execute(getConnName(),sql)

def getTimeFormat(targetDatetime):
    return targetDatetime.strftime("%Y-%m-%d")

# 커넥션 이름 획득
def getConnName():
    return "Event"


if __name__ == "__main__":
    db.init_db(getConnName())
    
    #insertEvent(("test eventname3","www.naver.com","2024-10-11","2244-12-14"))
    
    #print(selectEventList(),sep='\n')
    
    #insertEvent(("testname","https://www.naver.com",None,None,"0"))
    updateEventDate("레어 에그 ~다크 카니발~","1000-01-01","3000-12-31","2024-12-30")
    
    db.close(getConnName())
    print("test")