import crawling as cr

def crawling ():
    print("[INFO] crawlilng START")
    cr.init_driver()

    cr.move("https://pad.neocyon.com/W/notice/list.aspx")

    elements = cr.getElementsByTagName('tr')
    result = []
    for e in elements:        
        result.append(e.text.split())
        #print(e.text)
    print(result)
    return result
    
crawling()