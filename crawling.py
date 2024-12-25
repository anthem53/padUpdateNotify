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
    global driver
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

# 이동하려는 해당 웹페이지 주소 할당
def move(url):
    global driver
    driver.get(url)
    
#뒤로가기 
def back():
    global driver
    driver.back()
    
# 새로고침
def refresh():
    global driver
    driver.refresh()
    
# 앞으로가기
def forward():
    global driver
    driver.forward()

# 주어진 xpath에 해당하는 요소 가져옴.
def getElementByXpath(xpath):
    global driver
    # '''//*[@id="list"]/tbody'''
    elem = driver.find_element(By.XPATH,xpath)
    return elem
    
# 주어진 태그네임에해당하는 모든 요소를 리스트로 반환
def getElementsByTagName(tagName):
    global driver
    elements = driver.find_elements(By.TAG_NAME, tagName)
    return elements

def getDriverPageSource():
    global driver
    return driver.page_source

# 해당 시간 기다림.
def waitTag(tagName):
    global driver
    WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, tagName)))
    time.sleep(1)

# 정말 고정된 초 동안 기다림.
def waitSecond(second):
    time.sleep(second)
    
def quit():
    global driver
    driver.quit()

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
    
    
