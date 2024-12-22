import schedule
import threading
import time
import mail
import crawling_impl
import db_notify
import db
import log
import sys

def notify_job(is_debug = False):
    try:
        log.info("메일 발송 이벤트가 시작 되었습니다.")
        db.init_db()
        rawDatas = crawling_impl.crawling(is_debug);
        newDatas = db_notify.getNewDatas(rawDatas)
        if (len(newDatas) > 0 ):
            db_notify.clearData()
            db_notify.insertRawDatas(rawDatas)
            log.info("DB 삽입 완료, 메일 전송 전 ")
            mail.sendEmail(mail.generateMessage(newDatas),'퍼즐앤드래곤 신규 업데이트')
            log.info("메일 발송 이벤트가 완료 되었습니다.")
        else:
            log.info("업데이트된 내용이 없어 메일발송하지 않았습니다.")
        db.close()
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessageWithText(str(e)),"퍼즐앤드래곤 업데이트 감지 시스템 에러 발생")
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(e)
        db.close()


def schedule_notify():
    log.info("공지 크롤링 스케줄이 시작되었습니다.")
    schedule.every().day.at("18:00").do(notify_job)
    #schedule.every(1).miniutes.do(notify_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def getTaskJobThread():
    return threading.Thread(target=schedule_notify)

if __name__ == '__main__':
   
    if len(sys.argv) < 2:
        notify_job();
    else :
        notify_thread = threading.Thread(target=schedule_notify)
        notify_thread.start()
    
