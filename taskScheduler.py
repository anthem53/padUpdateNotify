import schedule
import threading
import time
import mail
import crawling_impl
import db_notify
import db
import log
import sys

#global
taskList = []

def setScheduleTask(name, job):
    global taskList
    taskList.append((name,job))

def scheduleStart():
    global taskList
    for name, job in taskList:
        log.info(name + " 스케줄이 시작되었습니다.")
        schedule.every().day.at("18:00").do(job)
        #schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def getScheduler():
    return threading.Thread(target=scheduleStart)

if __name__ == "__main__":
    
    print("test start")
    taskList = [("test", lambda : print("test")),("test2", lambda : print("test2"))]
    
    test_thread = getScheduler()
    test_thread.start()
    print("test end")