import crawling as cr
import log
from bs4 import BeautifulSoup
import re
import datetime
import db_event

EVENT_URL  = "https://pad.neocyon.com/W/event/list.aspx"

'''
TODO
DB와 연동해서 해당 항목이 DB에 존재하는지 확인.
만약 존재한다면 기간파싱 패스/ 없을 경우에만 기간 파싱 진행하도록 설정.

여기서 return 하는 데이터들은 현재 홈페이지에 있는 event들 정보.
'''

def crawling(oldEventNameList, isDebug = False):
    cr.init_driver()
    cr.move(EVENT_URL)
    cr.waitSecond(3)
    
    elements = cr.getElementsByTagName("a")
    targetUrls = []
    for e in elements:
        if ("[이벤트]" in e.text) :
            if isDebug :
                print(e.text)
            targetUrls.append((e.text.replace("[이벤트]", "").strip(), e.get_attribute('href')))
        
    result = []
    for title, targetUrl in targetUrls:
        if isDebug == True:
            print(title)
        if title not in oldEventNameList:
            log.info("%s page info" % (targetUrl))
            cr.move(targetUrl)
            cr.waitSecond(3)
            soup = BeautifulSoup(cr.getDriverPageSource(),'html.parser')
            soupStringList = soup.text.split('\n')
            p = re.compile('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]')
            datetimeList = []
            for sentence in soupStringList :
                if sentence == '':
                    continue
                dateInfo = p.findall(sentence)
                if len(dateInfo) >= 2 :
                    datetimeList.extend(dateInfo)
                    
            log.info("Page '%s' Done" % (title))
            
            result.append([title] + [targetUrl]+ findEventPeriod(datetimeList))
        else :
            result.append([title] + [None,None,None] )
    if isDebug == True:
        for elem in result:
            print(elem)
    
    return result
                
def findEventPeriod(periodInfo):
    if (len(periodInfo) == 0):
        return [None,None]
    
    DATE_FORMAT = "%Y/%m/%d"    
    startDate = datetime.date(3000,1,1)
    endDate = datetime.date(1970,1,1)
    
    # 시작날 확인
    for datetimeStr in periodInfo:
        curDate = datetime.datetime.strptime(datetimeStr,DATE_FORMAT).date()
        if curDate < startDate :
            startDate = curDate
        if endDate < curDate :
            endDate = curDate
        
    return [startDate,endDate]
            
if __name__ == "__main__":
    result = crawling([],True)
