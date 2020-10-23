from model.florexa_model import Appointments

class Book:
    def __init__(self,details):
        self.details =  details
        Appointments.connect()

    def schedule(self):
        print("dadadsad",self.details)
        doc = Appointments(self.details)
        doc.insert()
    
    def checkslot(self):
        
        pass
    
    def ismember(self):
        pass
    
    def confirm(self):
        pass
