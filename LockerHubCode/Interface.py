###Driver Code
class ReuseableObject:
    id = "123"
    image = "" #inBase64
    name = ""
    type = ""
    description = ""
    hasPin = True
    pin = "1"
    
    #Used on running
    toPut=True

    def __init__(self):pass
    def checkPin(self,pin):
        if not havePin: return True
        elif havePin and pin == self.pin: return True
        else: return False

class ImageRecognition:
    isAbuse = False
    image = ""
    def __init__(self):pass
    def check(self):
        self.isAbuse = False
im = ImageRecognition()


class DataBaseTemplate:
    def __init__(self):pass
    
    def registrationInDatabase(self,ID):
        return True
    def getRegistration(self,ID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.description = "This is a dummy object"
        return obj
        
    def objInDatabase(self,objID):
        output = True
        return output
    def readInObj(self,objID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.description = "This is a dummy object"
        return obj
    def writeOut(self,obj):
        print("Writing Out Object")
    def removeObject(self, obj):
        print("Removing Object",obj.id)
        
class DataBase(DataBaseTemplate):
    def objInDatabase(self,objID):
        data = anvil.server.call("getListings")
        for i in range(len(data)):
            if str(data[i]['lockerNumber']) == objID:
                return True
        return False
        
    def readInObj(self,objID):
        data = anvil.server.call("getListings")
        for i in range(len(data)):
            if str(data[i]['lockerNumber']) == objID:
                break
        obj = ReuseableObject()
        obj.name = data[i]["title"]
        #obj.image = "ImageData"
        obj.pin = data[i]["keyPin"]
        if obj.pin == None:
            obj.hasPin = False
        else:
            obj.hasPin = True
        obj.description = data[i]["description"]
        return obj
        
    def writeOut(self,obj):
        anvil.server.call("addRowIntoListings", obj.name, None,\
         obj.description,"WRYYYYYYYYYYY!",int(obj.id))
    def removeObject(self, obj):
        print("Removing Object",obj.id)
try:
    import anvil.server
    anvil.server.connect('NTC3GD3W7NUGZJYBRQS2L5KM-W5BOWXMEHYCQTPC4')
    db = DataBase()
except:
    print("Using Dummy Database")
    db = DataBaseTemplate()
    
import serial
class HardwareLocker:
    number = 0
    
    def serialWrite(self, write):
        self.ser.write(write.encode()) 
    def serialQuery(self,query):
        self.ser.write(query.encode())
        self.ser.flush() # it is buffering. required to get the data out *now*
        data = self.ser.readline() 
        return data
        
    def __init__(self, number):
        self.number = number
        
        try: self.ser = serial.Serial('/dev/ttyUSB0')  # open serial port
        except: 
            self.serialWrite = lambda write :None
            self.serialQuery = lambda query :b"Yes\r\n"
    def randomLocker(self):
        return "1" #return locker ID
    def hasObject(self, obj):
        data = self.serialQuery("check\n")
        state = data == b"Yes\r\n"
        #if obj.toPut==True: return True
        #else: return False
        return state
    def doorClosed(self):
        data = self.serialQuery("door\n")
        state = data == b"Yes\r\n"
        return state
    def lock(self):
        self.serialWrite('lock\n')    # write a string
    def unlock(self):
        self.serialWrite('unlock\n')     # write a string

hl = HardwareLocker(0)
