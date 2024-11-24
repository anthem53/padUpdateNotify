import crawling as cr
import log
from bs4 import BeautifulSoup
import re
import datetime

EVENT_URL  = "https://pad.neocyon.com/W/event/list.aspx"

def crawling_event():
    cr.init_driver()
    cr.move(EVENT_URL)
    cr.waitSecond(3)
    
    elements = cr.getElementsByTagName("a")
    targetUrls = []
    for e in elements:
        if ("[이벤트]" in e.text):
            targetUrls.append(e.get_attribute('href'))
        
    result = []
    for targetUrl in targetUrls:
        log.info("%s page info" % (targetUrl))
        cr.move(targetUrl)
        cr.waitSecond(3)
        soup = BeautifulSoup(cr.getDriverPageSource(),'html.parser')
        soupStringList = soup.text.split('\n')
        p = re.compile('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]')
        title= ""
        isFirst = True
        datetimeList = []
        for sentence in soupStringList :
            if sentence == '':
                continue
            if isFirst == True:
                isFirst = False;
                title = sentence
            if sentence.find("제목") != -1:
                title =  sentence.replace("제목","").strip()
                
            if sentence.find('기간') != -1:       
                dateInfo = p.findall(sentence)
                if len(dateInfo) > 0 :
                    datetimeList.extend(dateInfo)
                
        log.info("Page '%s' Done" % (title))
        
        result.append([title] + findEventPeriod(datetimeList))
    print(result,sep="\n")
    
    return result
                
def findEventPeriod(periodInfo):
    if (len(periodInfo) == 0):
        return [None,None]
    
    DATE_FORMAT = "%Y/%m/%d"    
    startDate = datetime.datetime(3000,1,1)
    endDate = datetime.datetime(1970,1,1)
    
    # 시작날 확인
    for i in range(0,len(periodInfo)):
        datetimeStr = periodInfo[i]
        curDatetime = datetime.datetime.strptime(datetimeStr,DATE_FORMAT)
        if curDatetime < startDate :
            startDate = curDatetime
        if endDate < curDatetime :
            endDate = curDatetime
        
    return [startDate,endDate]
            
    
if __name__ == "__main__":
    crawling_event()