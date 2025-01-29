import crawling as cr
import log

def crawling (isDebug = False):
    log.info("Notify Crawling START")
    #크롤링을 위한 셀레니움 객체 초기화.
    driver_instance = cr.init_driver()

    # 셀레니움 객체로 해당 사이트로 이동및 로딩을 위한 5초 기다림.
    cr.move(driver_instance, "https://pad.neocyon.com/W/notice/list.aspx")
    cr.waitTag(driver_instance, "tbody")
    #cr.waitSecond(5)

    # 공지 객체들이 tr 태그로 나와서 tr 객체 전부 조사
    elements = cr.getElementsByTagName(driver_instance, 'tr')

    # 결과 저장용 리스트 객체
    result = []
    for e in elements:       
        if isDebug == True:
           log.info(e.text) 
        else: pass

        temp = e.text.split()
        
        # NO과 title을 Key해서 No에 정수형 id가 없더라도 넣을 수 있도록 DB 처리함.
        if (temp[0] != "NO"):
            tempResult = []
            tempResult.append(temp[0])
            tempResult.append(" ".join(temp[1:-1]))
            tempResult.append(temp[-1])
            tempResult.append(e.text)
            result.append(tempResult)
    
        #print(e.text)
    log.info("Notify Crawling END")
    cr.quit(driver_instance)
    #시작타이틀 제외한 값만 넣기
    return result
    

if __name__ == "__main__":
    crawling(True)
    
