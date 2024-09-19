import sys
import schedule
import threading
import time
import mail
import crawling_impl
import db_notify


def currentTime():
    return "["+ time.strftime("%Y-%m-%d %H:%M:%S") + "]  "
    
def notify_job():
    try:
        print(currentTime() + "[INFO] 메일 발송 이벤트가 시작 되었습니다.")

        newDatas = db_notify.getNewDatas()
        #newDatas = []
        if (len(newDatas) > 0 ):
            mail.sendEmail(mail.generateMessage(newDatas))
            print(currentTime() +"[INFO] 메일 발송 이벤트가 완료 되었습니다.")
        else:
            print(currentTime() +"[INFO] 업데이트된 내용이 없어 메일발송하지 않았습니다.")
    except Exception as e:
        mail.sendEmail(mail.generateErrorMessage())
        print(currentTime() +"[ERROR] 에러로 인해 메일이 전송되지 않았습니다.")
        print(currentTime(), e)


def schedule_notify():
    print(currentTime() +"[INFO] 스케줄이 시작되었습니다.")
    schedule.every().day.at("18:00").do(notify_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
        


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        notify_job();
    else :
        notify_thread = threading.Thread(target=schedule_notify)
        notify_thread.start()

