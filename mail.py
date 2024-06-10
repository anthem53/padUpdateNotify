import smtplib
from email.mime.text import MIMEText
import crawling_impl
import db

def generateMessage():
    newDatas = crawling_impl.crawling()
    

    result = "신규 업데이트 내용\n\n"

    db.init_db()
    for id, title , date, ori in newDatas:
        
        if db.checkDup(int(id)) == False:
            result = result + "%s %s %s\n" %(id, title, date)

    db.clearData()
    for id, title , date,ori in newDatas:
        db.insertData(int(id),title,date,ori)

    db.close()
    
    return MIMEText(result)


def sendEmail():
    configInfo = dict()

    f= open("mail.config",'r')

    while True:
        line = f.readline().strip()
        print(line)
        if line =="":
            break
        else:
            parsed = line.split("=")
            configInfo[parsed[0]] = parsed[1]

    

    #587포트 및 465포트 존재
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    smtp.ehlo()

    smtp.starttls()

    #로그인을 통해 지메일 접속
    smtp.login(configInfo["from"], configInfo["password"])

    #내용을 입력하는 MIMEText => 다른 라이브러리 사용 가능
    #msg = MIMEText('내용 : 퍼즐앤드래곤 신규 업데이트')
    msg = generateMessage()
    msg['Subject'] = '퍼즐앤드래곤 신규 업데이트'

    #이메일을 보내기 위한 설정(Cc도 가능)
    smtp.sendmail(configInfo["from"], configInfo['to'], msg.as_string())

    #객체 닫기
    smtp.quit()


if __name__ == "__main__":
    sendEmail()
