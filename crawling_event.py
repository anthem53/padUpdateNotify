import crawling as cr
import log
from bs4 import BeautifulSoup
import re

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
        
    for targetUrl in targetUrls:
        log.info("%s page info" % (targetUrl))
        cr.move(targetUrl)
        cr.waitSecond(5)
        soup = BeautifulSoup(cr.getDriverPageSource(),'html.parser')
        soupStringList = soup.text.split('\n')
        p = re.compile('[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]')
        
        for sentence in soupStringList :
            if sentence == '':
                continue
            
            if sentence.find('기간') != -1:       
                result = p.findall(sentence)
                if len(result) > 0 :
                    print(result)
                
        log.info("Page %s Done" % (targetUrl))
                
if __name__ == "__main__":
    crawling_event()