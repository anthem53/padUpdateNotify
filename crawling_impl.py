import crawling as cr

def crawling ():
    print("[INFO] crawlilng START")
    cr.init_driver()

    cr.move("https://pad.neocyon.com/W/notice/list.aspx")
    cr.waitSecond(5)

    elements = cr.getElementsByTagName('tr')
    result = []
    for e in elements:        
        temp = e.text.split()
        tempResult = []
        tempResult.append(temp[0])
        tempResult.append(" ".join(temp[1:-1]))
        tempResult.append(temp[-1])
        tempResult.append(e.text)
        try:
            int(temp[0])
            result.append(tempResult)
        except : 
            pass
        #print(e.text)
    print("[INFO] crawlilng END")
    return result[1:]
    

if __name__ == "__main__":
    crawling()
