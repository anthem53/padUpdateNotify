import crawling as cr
import log
from bs4 import BeautifulSoup
import re
import datetime
from custom_code.event_code import EventResultCode


EVENT_URL  = "https://pad.neocyon.com/W/event/list.aspx"

# returnValue = [title] + [targetUrl] + [startDATE] [endDate] +[updateDate] + [resultCode]
def crawling(exceptionWordList:list = [] ,isDebug = False):
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
            log.info("%s page info" % (targetUrl))
        if (targetUrl == 'https://pad.neocyon.com/W/event/view.aspx?id=2300') :
            print("TARGET")
            
        isExcept = False
        for exceptionWord in exceptionWordList:
            if exceptionWord in title:
                isExcept = True 
                break
            else:pass
            
        if isExcept == True:
            continue
            
        result.append(execute_crawl(driver_instance,title,update_date,targetUrl))
            
        if isDebug == True:
            log.info("Page '%s' Done" % (title))
            
        
    if isDebug == True:
        for elem in result:
            print(elem)
    
    log.info("Event Crawling End")
    cr.quit(driver_instance)
    return result

#실제 crawl 하는 부분. 
def execute_crawl(driver_instance,title,update_date,targetUrl):
    cr.move(driver_instance, targetUrl)
    cr.waitSecond(driver_instance, 3)
    soup = BeautifulSoup(cr.getDriverPageSource(driver_instance),'html.parser')
    soupStringList = soup.text.split('\n')
    p1 = re.compile('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]')
    p2 = re.compile('[0-9][0-9]/[0-9][0-9]')
    p_list = [p1,p2]
    datetimeList = []
    for sentence in soupStringList :
        if sentence == '':
            continue
        for p in p_list :
            dateInfo = p.findall(sentence)
            if len(dateInfo) >= 2 :
                datetimeList.extend(dateInfo)
    print(title)
    return [title] + [targetUrl] + find_event_period(datetimeList) + [update_date]
          
def find_event_period(periodInfo):
    if (len(periodInfo) == 0):
        return [None,None]
    
    current_year = datetime.datetime.now().year
    DATE_FORMAT = "%Y/%m/%d"
    DATE_FORMAT2 = "%m/%d"
    date_format_list = [(DATE_FORMAT,'[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]'), (DATE_FORMAT2,'[0-9][0-9]/[0-9][0-9]')]
    startDate = datetime.date(3000,1,1)
    endDate = datetime.date(1970,1,1)
    
    # 시작날 확인
    for datetimeStr in periodInfo:
        elements = datetimeStr.split("/")
        
        try:
            if len(elements) == 3 :
                curDate = datetime.datetime.strptime(datetimeStr,DATE_FORMAT).date()
            elif len(elements) == 2: 
                curDate = datetime.datetime.strptime(str(current_year)+"/"+datetimeStr,DATE_FORMAT).date()
            else :
                raise Exception
            if curDate < startDate :
                startDate = curDate
            if endDate < curDate :
                endDate = curDate
        except Exception:
            log.error("[crawling_event#find_event_period] 오류 Error 원인 : {0}".format(datetimeStr))
            
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
    #testdict["퍼즐앤드래곤 대감사제"] = "2024-12-24"
    result = crawling([],True)
    #__crawlingEventTest__()
    
