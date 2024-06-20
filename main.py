import schedule
import threading
import time
import mail


    
def notify_job():
    try:
        mail.sendEmail(mail.generateMessage())
    except :
        mail.sendEmail(mail.generateErrorMessage())
        print("mail 전송이 되지 아니하였습니다.")


def schedule_notify():
    schedule.every().day.at("18:00").do(notify_job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    
        
notify_thread = threading.Thread(target=schedule_notify)

