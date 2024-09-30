import crawling as cr
import log

def crawling (isDebug = False):
    log.info("Crawling START")
    #크롤링을 위한 셀레니움 객체 초기화.
    cr.init_driver()

    # 셀레니움 객체로 해당 사이트로 이동및 로딩을 위한 5초 기다림.
    cr.move("https://pad.neocyon.com/W/notice/list.aspx")
    cr.waitSecond(5)

    # 공지 객체들이 tr 태그로 나와서 tr 객체 전부 조사
    elements = cr.getElementsByTagName('tr')

    # 결과 저장용 리스트 객체
    result = []
    for e in elements:       
        if isDebug == True:
           log.info(e.text) 
        else: pass

        temp = e.text.split()
        # 만약 NO에 공지라고 되어있으면 예외처리, 아닌 경우만 result에 넣기
        if(temp[0].isdigit()):
            int(temp[0])
            tempResult = []
            tempResult.append(temp[0])
            tempResult.append(" ".join(temp[1:-1]))
            tempResult.append(temp[-1])
            tempResult.append(e.text)
            result.append(tempResult)
        else:
            pass
        #print(e.text)
    log.info("Crawling END")
    #시작타이틀 제외한 값만 넣기
    return result[1:]
    

if __name__ == "__main__":
    crawling(False)
