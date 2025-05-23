import schedule
import threading
import time
import log

class Scheduler (threading.Thread):
    def __init__(self,isDebug = False):
        super().__init__()
        self.taskList = []
        self.status = True
        self.isDebug = isDebug
        self.name = "Scheduler"
        
    def setScheduleTask(self,name, job,period):
        self.taskList.append((name,job,period))
        
    def run (self):
        if (self.isDebug == False):
            for name, job,period in self.taskList:
                log.info(name + " 스케줄이 시작되었습니다.")
                schedule.every().day.at(period).do(job)
        else:
            for name, job,period in self.taskList:
                log.info(name + " 스케줄이 시작되었습니다.")
                schedule.every(1).minutes.do(job)
        while self.status:
            schedule.run_pending()
            time.sleep(1)
            
    def setStatus(self,status:bool):
        self.status = status

if __name__ == "__main__":
    
    print("test start")
    worker = Scheduler()
    worker.setScheduleTask("test", lambda : print("test"),"18:00")
    worker.setScheduleTask("test2", lambda : print("test2"),"18:00")
    worker.setScheduleTask("test3", lambda : print("test3"),"18:00")
    
    worker.run()
    print("test end")