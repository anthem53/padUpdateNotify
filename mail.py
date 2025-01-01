import smtplib
from email.mime.text import MIMEText
from customCode.event_code import EventTaskResultCode

# Create MimeText element with processded string message.
def generateMessage(newDatas):
    
    result = "신규 업데이트 내용\n\n"
    
    # 신규 내용이 있는 경우 
    if len(newDatas) > 0 :
        # 해당 내용을 메일 내용에 추가
        for id, title , date, ori in newDatas:
            result = result + "%d %s %s\n" %(id, title, date)
    else : 
        result += "새로운 업데이트 내용이 없습니다."
    
    result += "\n\n\n 퍼즐앤드래곤 공식 홈페이지 사이트 : https://pad.neocyon.com/W/notice/list.aspx"
    
    return MIMEText(result)

def  generateEventMessage(result):
    msg = "일정이 변경된 이벤트 리스트\n\n\n"

    if len(result[EventTaskResultCode.START.value]) > 0 :
        msg += "● 새로 등록된 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.START.value]:
            msg += "\t - %s : %s\n" % (name,link)
            
            
    if len(result[EventTaskResultCode.CLOSE.value]) > 0 :
        msg += "● 종료된 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.CLOSE.value]:
            msg += "\t - %s : %s\n" % (name,link)
            
    if len(result[EventTaskResultCode.NEED.value]) > 0 :
        msg += "● 입력 필요한 이벤트리스트\n"
        for name, link in result[EventTaskResultCode.NEED.value]:
            msg += "\t - %s : %s\n" % (name,link)
    
    if (len(result[EventTaskResultCode.UPDATE.value]) > 0 ):
        msg += "● 내용이 업데이트 된 이벤트 리스트\n"
        for name,link, startDate, endDate,updateDate in result[EventTaskResultCode.UPDATE.value]:
            msg += "\t - [%s] 이벤트가 %s 에 업데이트 되었습니다.해당 이벤트 종료일은 %s 입니다. : %s\n" % (name,updateDate,endDate,link)
        
    msg += "\n\n\n 퍼즐앤드래곤 공식 홈페이지 이벤트 사이트 : https://pad.neocyon.com/W/event/list.aspx"    
    return MIMEText(msg)

# 에러 알림 메시지 + 해당 내용
def generateErrorMessageWithText(errorText:str):
    content = "에러로 인해 업데이트 체크 시스템이 종료되었습니다. 확인 해주십시오.\n\n- 에러 내용\n\n"
    
    content += str(errorText)
    
    return MIMEText(content)

# send Error message
def generateErrorMessage():
    return MIMEText("에러로 인해 업데이트 체크 시스템이 종료되었습니다. 확인 해주십시오.")


# send given Message without processing process
def generateCustomMessage(content:str):
    return MIMEText(content)

# message is MIMEText type
def sendEmail(message:MIMEText,title):
    configInfo = dict()

    f= open("mail.config",'r')

    while True:
        line = f.readline().strip()
        #print(line)
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
    msg = message
    msg['Subject'] = title

    #이메일을 보내기 위한 설정(Cc도 가능)
    smtp.sendmail(configInfo["from"], configInfo['to'], msg.as_string())

    #객체 닫기
    smtp.quit()




if __name__ == "__main__":
    sendEmail(generateCustomMessage('일정이 변경된 이벤트 리스트\n\n\n종료된 이벤트리스트\n서비스 12주년 기념 스페셜 세트 판매! : https://pad.neocyon.com/W/event/view.aspx?id=2235\n'),"퍼드 이벤트 변동")
