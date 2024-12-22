import sys
import task
import taskEvent
import atexit
import log
import mail
import statusTest
import taskScheduler

def endFunction():
    mail.sendEmail(mail.generateCustomMessage("퍼즐앤드래곤 크롤링 서버가 종료되었습니다."),"퍼즐앤드래곤 크롤링 종료")
    log.info("프로그램이 특정 이유로 종료 되었습니다.");

if __name__ == '__main__':
    try :
        statusTest.execute()
        if len(sys.argv) < 2: 
            task.notify_job();
            taskEvent.notify_event_job()
        else :
            atexit.register(endFunction)
            taskScheduler.setScheduleTask("공지 크롤링",task.notify_job)
            taskScheduler.setScheduleTask("이벤트 크롤링",taskEvent.notify_event_job)
            
            schedulerThread = taskScheduler.getScheduler()
            schedulerThread.start()
    except Exception as e:
        log.error("서비스 설정 테스트 중 에러가 발생하였습니다.")
        log.write(e)

