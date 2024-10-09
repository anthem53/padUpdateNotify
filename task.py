import schedule
import threading
import time
import mail
import crawling_impl
import db_notify
import log


def notify_job():
    try:
        log.info("메일 발송 이벤트가 시작 되었습니다.")
        rawDatas = crawling_impl.crawling();
        newDatas = db_notify.getNewDatas(rawDatas)
        if (len(newDatas) > 0 ):
            db_notify.insertRawDatas(rawDatas)
            mail.sendEmail(mail.generateMessage(newDatas))
            log.info("메일 발송 이벤트가 완료 되었습니다.")
        else:
            log.info("업데이트된 내용이 없어 메일발송하지 않았습니다.")
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessage())
        log.error("에러로 인해 메일이 전송되지 않았습니다.")
        log.write(e)


def schedule_notify():
    log.info("스케줄이 시작되었습니다.")
    schedule.every().day.at("18:00").do(notify_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

def getTaskJobThread():
    return threading.Thread(target=schedule_notify)

if __name__ == '__main__':
    notify_job()
    '''
    if len(sys.argv) < 2:
        notify_job();
    else :
        notify_thread = threading.Thread(target=schedule_notify)
        notify_thread.start()
    '''
