import crawling as cr

def crawling ():
    print("[INFO] crawlilng START")
    cr.init_driver()

    cr.move("https://pad.neocyon.com/W/notice/list.aspx")

    elements = cr.getElementsByTagName('tr')
    result = []
    for e in elements:        
        temp = e.text.split()
        tempResult = []
        tempResult.append(temp[0])
        tempResult.append(" ".join(temp[1:-1]))
        tempResult.append(temp[-1])
        tempResult.append(e.text)
        result.append(tempResult)
        #print(e.text)
    print(*result[1:],sep="\n")
    return result[1:]
    

if __name__ == "__main__":
    crawling()
