import sys
import task
import taskEvent
import atexit
import log
import mail
import statusTest
import schedule

def endFunction():
    mail.sendEmail(mail.generateCustomMessage("퍼즐앤드래곤 크롤링 서버가 종료되었습니다."),"퍼즐앤드래곤 크롤링 종료")
    log.info("프로그램이 특정 이유로 종료 되었습니다.");

atexit.register(endFunction)

if __name__ == '__main__':
    try :
        statusTest.execute()
        if len(sys.argv) < 2: 
            task.notify_job();
            taskEvent.notify_event_job()
        else :
            notify_thread = task.getTaskJobThread()
            notify_thread.start()
            
            eventThread = taskEvent.getTaskJobThread()
            eventThread.start()
    except Exception as e:
        log.error("서비스 설정 테스트 중 에러가 발생하였습니다.")
        log.write(e)

