import sys
import task
import taskEvent
import atexit
import log
import mail
import statusTest
import taskScheduler
import time

def endFunction(isDebug = False):
    if (isDebug == False):
        mail.sendEmail(mail.generateCustomMessage("퍼즐앤드래곤 크롤링 서버가 종료되었습니다."),"퍼즐앤드래곤 크롤링 종료")
        log.info("퍼즐앤드래곤 공지 게시판 알림 프로그램이 종료 되었습니다.");
    else :
        pass

if __name__ == '__main__':
    try :
        isDebug = False
        statusTest.execute()
        if len(sys.argv) < 2: 
            task.notify_job();
            taskEvent.notify_event_job()
        else :
            if len(sys.argv) == 3: 
                log.debug("Debug Mode On")
                isDebug = True
            
            atexit.register(lambda : endFunction(isDebug))
            scheduleWorker = taskScheduler.scheduler(isDebug)
            scheduleWorker.setScheduleTask("공지 크롤링",task.notify_job,"18:00")
            scheduleWorker.setScheduleTask("이벤트 크롤링",taskEvent.notify_event_job,"18:00")
            
            
            scheduleWorker.start()
            while True:
                try :
                    time.sleep(1)
                except KeyboardInterrupt:
                    log.info("KeyboardInterrupt로 모든 작업이 중지 되었습니다.")
                    scheduleWorker.setStatus(False)
                    quit()
                
    except Exception as e:
        log.error("서비스 설정 테스트 중 에러가 발생하였습니다.")
        log.write(e)

