class Event:
    def __init__(self,name,link=None, status=None, startDate=None, endDate=None,updateDate=None):
        if (link != None) :
            self.name = name
            self.link = link
            self.status = status
            self.startDate = startDate
            self.endDate = endDate
            self.UpdateDate= updateDate
        else :
            self.name = name[0]
            self.link = name[1]
            self.status = name[2]
            self.startDate = name[3]
            self.endDate = name[4]
            self.updateDate= name[5]
        
        
