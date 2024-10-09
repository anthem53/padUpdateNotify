# 소개

한국 퍼즐앤드래곤 사이트의 업데이트를 감지하여 해당 목록을 대략적으로 메일로 알려주는 프로젝트


# 환경
python 3.10
우분투 22.04

# 사용 DB 
mysql

# 라이브러리
- schedule
- selenium
- webdriver_manager
- pymysql

라이브러리 다운로드 코드
```
pip install schedule ,selenium ,webdriver_manager,pymysql
```

# 설정 파일
db.config , mail.config를 해당 project 내 만들어야함. 

## db.config
```
id=db_id
password=db_password
```
  
## mail.config
```
from=메일발송자
to=메일받을사람
password=해당 메일stmp password
```
