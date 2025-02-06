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
라이브러리 다운로드 코드
```
pip install schedule selenium webdriver_manager pymysql beautifulsoup4 cryptography
```

# 설정 파일
db.config , mail.config를 해당 project 내 생성해야함.

## db.config
```
host=db_host
id=db_id
password=db_password
```
DB 종류는 MySQL.

만약 같은 서버 내 실행이라면 db_host 자리에 localhost나 127.0.0.1 입력
  
## mail.config
```
from=메일발송주체가 될 이메일 주소
to=메일 받을 이메일 주소
password=해당 메일stmp password
```

현 시점 한 서버당 하나의 유저에게 mail보내도록 되어있음. 이유는 메일서버가 개인 email의 stmp 서버라 구글 정책이 적용되는데 메일 전송 최대 제한이 존재하여 이리 설정.

## exceptionWord.config

TODO 
- 이벤트 크롤링 한정 config인데, 관련 키워드를 파일명에 추가하면 좋을듯.

이벤트 크롤링시 제외할 문구를 ,로 나열한 파일임. 따라서 별다른 줄은 없으며 로직 실행시 해당 파일을 읽어 처리하기 때문에 재기동 없이 수정 반영 가능. 

예시
```
카니발, 퀘스트
```
- 이 경우 ,로 단어를 분리하며 단어 앞 뒤 공백을 제거한 값으로 비교함.
- 크롤링시 해당 단어가 제목에 포함되어있을 경우 크롤링 로직에서 제외, 결과에서도 아예 포함시키지 않음.
- 해당 파일 존재하지 않을 경우 제외 필터링할 단어가 없는 것으로 처리 진행.
  


