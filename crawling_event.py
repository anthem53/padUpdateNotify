import crawling as cr
import log
from bs4 import BeautifulSoup
import re
import datetime
from customCode.event_code import EventResultCode


EVENT_URL  = "https://pad.neocyon.com/W/event/list.aspx"

# returnValue = [title] + [targetUrl] + [startDATE] [endDate] +[updateDate] + [resultCode]
def crawling(oldEventNameDateMap, isDebug = False):
    driver_instance = cr.init_driver()
    cr.move(driver_instance, EVENT_URL)
    cr.waitSecond(driver_instance, 3)
    log.info("Event Crawling Start")
    elements = cr.getElementsByTagName(driver_instance, "li")
    targetUrls = []
    for e in elements:
        if ("[이벤트]" in e.text) :
            if isDebug :
                print(e.text)
            title,rawDate = e.text.split("\n")
            title = title.replace("[이벤트]", "").strip()
            update_date = rawDate.replace("등록일","").strip()
            targetUrl = cr.getChildElmentByTagName(e,"a")[0].get_attribute('href')
            targetUrls.append((title,update_date,targetUrl))
        
    result = []
    for title,update_date ,targetUrl in targetUrls:
        if isDebug == True:
            print(title)
        if title not in oldEventNameDateMap:
            result.append(execute_crawl(driver_instance,title,update_date,targetUrl,EventResultCode.NEW))
        elif title in oldEventNameDateMap and update_date != oldEventNameDateMap[title]:
            # start 
            result.append(execute_crawl(driver_instance,title,update_date,targetUrl,EventResultCode.UPDATE))
        else :
            result.append([title] + [None,None,None,None,EventResultCode.EXIST])
            
        
    if isDebug == True:
        for elem in result:
            print(elem)
    
    log.info("Event Crawling End")
    cr.quit(driver_instance)
    return result

#TODO
def execute_crawl(driver_instance,title,update_date,targetUrl,resultCode):
    log.info("%s page info" % (targetUrl))
    cr.move(driver_instance, targetUrl)
    cr.waitSecond(driver_instance, 3)
    soup = BeautifulSoup(cr.getDriverPageSource(driver_instance),'html.parser')
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
    
    return [title] + [targetUrl] + findEventPeriod(datetimeList) + [update_date] + [resultCode]
          
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

def __crawlingEventTest__():
    driver_instance = cr.init_driver()
    cr.move(driver_instance, EVENT_URL)
    cr.waitSecond(driver_instance, 3)
    log.info("Event Crawling Start")
    elements = cr.getElementsByTagName(driver_instance, "li")
    targetUrls = []
    for e in elements:
        if ("[이벤트]" in e.text) :
            name,rawDate = e.text.split("\n")
            name = name.replace("[이벤트]", "")
            update_date = rawDate.replace("등록일","")
            link = cr.getChildElmentByTagName(e,"a")[0].get_attribute('href')
            targetUrls.append((name,update_date,link))
            
    print(targetUrls)
    cr.quit(driver_instance)
    
if __name__ == "__main__":
    testdict = dict()
    testdict["퍼즐앤드래곤 대감사제"] = "2024-12-24"
    result = crawling([],testdict,True)
    #__crawlingEventTest__()
    
