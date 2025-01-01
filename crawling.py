# https://pad.neocyon.com/W/notice/list.aspx

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Chrome driver 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager 

# 페이지 로딩 기다리기
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import log

# 전역으로 변수 선언.
driver = None

# 셀레니움 드라이브 초기화
def init_driver(): 
    driver = None
    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # 자동으로 안꺼지는 옵션
    chrome_options.add_argument("--incognito") #시크릿 모드의 브라우저가 실행됩니다.
    chrome_options.add_argument("--headless") # 디스플레이 없는 환경이라 이거 필수
    chrome_options.add_argument("--no-sandbox") # 이거 없으면 셀레니움에서 경고를 보냄.
    chrome_options.add_argument("--disable-dev-shm-usage"); #/deb/shm 디렉토리를 사용하지 않음. 이 디렉토리는 공유 메모리를 담당하는 부분이다.
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 콘솔로그 출력 안하게
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 제어 메시지 제거
    chrome_options.add_experimental_option("useAutomationExtension", False)  # 자동화 확장기능 비활성화
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 자동화 탐지 회피

    service = Service(excutable_path=ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=service, options = chrome_options)
    
    return driver

# 이동하려는 해당 웹페이지 주소 할당
def move(driver, url):
    driver.get(url)
    
#뒤로가기 
def back(driver):
    driver.back()
    
# 새로고침
def refresh(driver):
    driver.refresh()
    
# 앞으로가기
def forward(driver):
    driver.forward()

# 주어진 xpath에 해당하는 요소 가져옴.
def getElementByXpath(driver, xpath):
    # '''//*[@id="list"]/tbody'''
    elem = driver.find_element(By.XPATH,xpath)
    return elem
    
# 주어진 태그네임에 해당하는 모든 요소를 리스트로 반환
def getElementsByTagName(driver, tagName):
    elements = driver.find_elements(By.TAG_NAME, tagName)
    return elements

# 특정 요소의 특정 태그를 가진 자식 요소를 획득
def getChildElmentByTagName(parent, tagName):
    children = parent.find_elements(By.TAG_NAME, tagName)
    return children

# 해당 드라이버의 page_source 획득
def getDriverPageSource(driver):
    return driver.page_source

# 해당 시간 기다림.
def waitTag(driver, tagName):
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, tagName)))
    time.sleep(1)

# 정말 고정된 초 동안 기다림. driver는 사용하지 않으나 다른 함수와 동일한 매개변수 구조를 위해 삽입.
def waitSecond(driver, second):
    time.sleep(second)
    
# 해당 크롤링 드라이버 종료. 크롤링 로직 종료시 반드시 호출 해야함.
def quit(driver):
    driver.quit()
    
def crawlTest():
    log.info("Crawling 연결 테스트 시작 합니다.")
    try :
        test_driver = init_driver()
        quit(test_driver)
        log.info("Crawling 연결이 정상적입니다.")
    except Exception as e :
        log.error("Crawling 연결 실패 하였습니다.")
        raise e   


#driver.get("http://naver.com")


if __name__ == "__main__":
    
    
    log.info("start")
    init_driver();
    url = "https://pad.neocyon.com/W/notice/list.aspx"
    log.info("Move")
    move(url)
    
    log.info("Waiting")
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
    
   # time.sleep(5)
    log.info("crawling End")
    log.info("Result :")
    elements = driver.find_elements(By.TAG_NAME, 'tr')
    for e in elements:
        print(e.text)
        print()
    
    
