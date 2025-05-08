import sys
import task_notice
import task_event
import atexit
import log
import mail
import status_test
import time
import traceback
from scheduler import Scheduler

def endFunction(isDebug = False):
    if (isDebug == False):
        mail.sendEmail(mail.generate_custom_message("퍼즐앤드래곤 크롤링 서버가 종료되었습니다."),"퍼즐앤드래곤 크롤링 종료")
        log.info("퍼즐앤드래곤 공지 게시판 알림 프로그램이 종료 되었습니다.");
    else :
        pass

if __name__ == '__main__':
    try :
        status_test.execute()
    except Exception as e:
        log.error("서비스 설정 테스트 중 에러가 발생하였습니다.")
        log.write(e)
        quit()
        
    try :
        if len(sys.argv) < 2: 
            task_notice.notify_job();
            task_event.notify_event_job()
        else :
            isDebug = False
            if len(sys.argv) == 3: 
                log.debug("Debug Mode On")
                isDebug = True
            atexit.register(lambda : endFunction(isDebug))
            scheduleWorker = Scheduler(isDebug)
            scheduleWorker.setScheduleTask("공지 크롤링",task_notice.notify_job,"18:00")
            scheduleWorker.setScheduleTask("이벤트 크롤링",task_event.notify_event_job,"18:00")
            scheduleWorker.start()
            
            #메인 thread에서 Keyboard Interrupt 발생시 스케쥴러도 종료할 수 있도록 처리.
            while True:
                try :
                    time.sleep(1)
                except KeyboardInterrupt:
                    log.info("KeyboardInterrupt로 모든 작업이 중지 되었습니다.")
                    scheduleWorker.setStatus(False)
                    quit()
    except Exception as e:
        log.error("스케쥴러 실행 중 에러 발생하였습니다.")
        log.write(traceback.format_exc())
        quit()
    

