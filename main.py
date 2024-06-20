import schedule
import threading
import time
import mail


    
def notify_job():
    try:
        print("[INFO] 메일 발송 이벤트가 시작 되었습니다.")
        mail.sendEmail(mail.generateMessage())
        print("[INFO] 메일 발송 이벤트가 완료 되었습니다..")
    except :
        mail.sendEmail(mail.generateErrorMessage())
        print("mail 전송이 되지 아니하였습니다.")


def schedule_notify():
    schedule.every().day.at("18:00").do(notify_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
        
notify_thread = threading.Thread(target=schedule_notify)

notify_thread.start()

