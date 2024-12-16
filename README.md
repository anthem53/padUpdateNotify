# 소개

한국 퍼즐앤드래곤 사이트의 업데이트를 감지하여 해당 목록을 대략적으로 메일로 알려주는 프로젝트

현재 감지 대상은 공지 첫 페이지와, 이벤트 항목임.  공지 첫페이지는 추가/변경/삭제 등 기존과 변경된 사항 발생시 알림, 이벤트는 새로 생긴 이벤트 발생시 알림.

# 환경
python 3.10
우분투 22.04
->  python 3.10 window 10

# 사용 DB 
mysql

# 라이브러리
- schedule
- selenium
- webdriver_manager
- pymysql

라이브러리 다운로드 코드
```
pip install schedule selenium webdriver_manager pymysql beautifulsoup4 cryptography
```

# 설정 파일
db.config , mail.config를 해당 project 내 만들어야함. 

## db.config
```
host=db_host
id=db_id
password=db_password
```
만약 같은 서버 내 돌아간다면 db_host 자리에 localhost나 127.0.0.1 입력
  
## mail.config
```
from=메일발송자
to=메일받을사람
password=해당 메일stmp password
```
