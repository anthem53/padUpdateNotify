import db
import log
from datetime import date
from model.event import Event

table_name = "event"
dev_table_name = 'event_dev'

def init():
    db.init_db(get_conn_name())
    
def close ():
    db.close(get_conn_name())

def existEvent(eventName ,is_debug = False):
    sql = "SELECT 1 FROM "+ get_target_table(is_debug) + " WHERE name = %s"
    db.execute(get_conn_name(),sql,(eventName))
    result = db.fetchall(get_conn_name())
    return len(result) > 0


#Event(name, link ,status, startDate, endDate, updateDate)
def insertEvent(event:Event,is_debug = False):
    log.info("Insert event : " + event.name)
    sql = "INSERT INTO "+ get_target_table(is_debug) + " (name, link, status, start_date, end_date, update_date) values (%s,%s,%s,%s,%s,%s)"     
    db.execute(get_conn_name(),sql,(event.name, event.link, event.status, event.startDate,event.endDate,event.updateDate))
        

#단건 조회
def selectEvent(name,is_debug = False):
    sql = "SELECT * FROM "+ get_target_table(is_debug) + " WHERE name = %s" 
    db.execute(get_conn_name(),sql,(name))
    result = db.fetchall(get_conn_name())
    return result   


#다건조회
def selectEventList(is_debug = False):
    sql = "SELECT * FROM "+ get_target_table(is_debug)
    db.execute(get_conn_name(),sql)
    result = db.fetchall(get_conn_name())
    return result   

#다건조회 Only name
def selectEventNameList(is_debug = False):
    sql = "SELECT name FROM "+ get_target_table(is_debug) 
    db.execute(get_conn_name(),sql)
    result = db.fetchall(get_conn_name())
    return [elem[0] for elem in result]

#다건 조회 with Map
def selectEventNameDateList(is_debug = False):
    sql = "SELECT name,update_date FROM "+ get_target_table(is_debug)
    db.execute(get_conn_name(),sql)
    result = db.fetchall(get_conn_name())
    resultMap = dict()
    for elem in result:
        resultMap[elem[0]] = elem[1].strftime("%Y-%m-%d")
    return resultMap


#오픈중인 이벤트
def isOpenEvent(name,startDate,endDate,is_debug = False):
    sql = "SELECT 1 FROM "+ get_target_table(is_debug) + " WHERE name = '%s' AND startDate >= '%s' AND endDate <='%s'" % (name,startDate, endDate)
    db.execute(get_conn_name(),sql)
    result = db.fetchall(get_conn_name())
    return len(result) > 0

# event endDate 업데이트
def updateEventDate(name, endDate,updateDate,is_debug = False):
    sql = "UPDATE "+ get_target_table(is_debug) + " SET end_date = %s, update_date = %s WHERE name = %s"
    db.execute(get_conn_name(),sql,(endDate,updateDate,name))
    
# event 업데이트
def update_event(name,link, end_date,update_date,is_debug = False):
    sql = "UPDATE "+ get_target_table(is_debug) + " SET link = %s, end_date = %s, update_date = %s WHERE name = %s"
    db.execute(get_conn_name(),sql,(link, end_date, update_date,name))

#이벤트 status 수정
def updateEventStatus(name, status,is_debug = False):
    sql = "UPDATE "+ get_target_table(is_debug) + " SET status = '%s' WHERE name = '%s'" % (str(status), name)
    db.execute(get_conn_name(),sql)
    

#이벤트 삭제
def deleteEvent(name,is_debug = False):
    log.info("delete event [%s]" % (name))
    sql = "DELETE FROM "+ get_target_table(is_debug) + " WHERE name = '%s'" %(name)
    db.execute(get_conn_name(),sql)

# target Table 이름
def get_target_table (is_debug):
    global table_name, dev_table_name
    if is_debug == True:
        return dev_table_name
    else:
        return table_name

# 커넥션 이름 획득
def get_conn_name():
    return "Event"


if __name__ == "__main__":
    db.init_db(get_conn_name())
    
    #insertEvent(("test eventname3","www.naver.com","2024-10-11","2244-12-14"))
    result = existEvent("6월의 퀘스트 개최!",False)
    print(result)
    #insertEvent(Event("test","https://www.naver.com","0",date.today(),date.today(),date.today()))
    
    #print(selectEventList(),sep='\n')
    
    #insertEvent(("testname","https://www.naver.com",None,None,"0"))
    #updateEventDate("레어 에그 ~다크 카니발~","1000-01-01","3000-12-31","2024-12-30")
    
    db.close(get_conn_name())
    print("test")