import mail

def endFunction():
    mail.sendEmail(mail.generateCustomMessage("퍼즐앤드래곤 크롤링 서버가 중료되었습니다."))


if __name__ == "__main__":
    endFunction()

