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

    def __init__(self, id="123"):
        self.id = id
    def checkPin(self,pin):
        if not havePin: return True
        elif havePin and pin == self.pin: return True
        else: return False
'''
class ImageRecognition:
    isAbuse = False
    image = ""
    def __init__(self):pass
    def check(self):
        self.isAbuse = False
'''
from classify_image import *
maybe_download_and_extract()
allowed = ["radio", "cellular phone","cell", "mobile computer", "handheld computer", "iPod", "casette","projector","television", "monitor","screen",'punching bag', 'punch bag', 'punching ball', 'punchball', 'balloon', 'hair spray', 'bathing cap', 'swimming cap', 'seat belt', 'seatbelt',]
class ImageRecognition:
    isAbuse = False
    image = ""
    def __init__(self):pass
    def check(self):
        possiblePredictions=""
        listOfPredictions = []
        try:
            os.system("raspistill -o /tmp/output.jpeg")
            predictionsData = run_inference_on_image("/tmp/output.jpeg")
            for prediction, score in predictionsData:
                possiblePredictions += prediction+","
            listOfPredictions = [i.strip() for i in possiblePredictions.split(",")]
        except:
            listOfPredictions = []
        print(listOfPredictions)
        commonThings = list(set(listOfPredictions).intersection(allowed))
        if len(commonThings) > 0:
            self.isAbuse = False
        else:
            self.isAbuse = True
            
im = ImageRecognition()
import datetime
class DataBaseTemplate:
    def __init__(self):pass
    
    def registrationInDatabase(self,ID):
        return True
    def getRegistration(self,ID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.description = "This is a dummy object, and it has very very long text for it to be used in testing"
        return obj
        
    def objInDatabase(self,objID):
        output = True
        return output
    def readInObj(self,objID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.description = "This is a dummy object, and it has very very long text for it to be used in testing"
        return obj
    def writeOut(self,obj):
        print("Writing Out Object")
    def removeObject(self, obj):
        print("Removing Object",obj.id)

import datetime
class DataBase(DataBaseTemplate):
    def __init__(self):
        self.fireDB = firestore.client()
        self.retrieveWholeDatabase()
        self.bucket = storage.bucket()
    def registrationInDatabase(self,ID):
        return True
    def getRegistration(self,ID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.description = "This is a dummy object, and it has very very long text for it to be used in testing"
        return obj
        
    def retrieveWholeDatabase(self):
        self.docs = self.fireDB.collection(u'listings').get()
    def objInDatabase(self,objID):
        self.retrieveWholeDatabase()
        for doc in self.docs:
            if str(doc.to_dict().get('lockerNumber')) == str(objID):
                return True
        return False
        
    def readInObj(self,objID):
        self.retrieveWholeDatabase()
        for doc in self.docs:
            if str(doc.to_dict().get('lockerNumber')) == str(objID):
                break
        obj = ReuseableObject() 
        obj.id = doc.to_dict().get('lockerNumber')
        obj.name = doc.to_dict().get('title')
        obj.description = doc.to_dict().get("descrip")
        obj.pin = doc.to_dict().get("keyPin")
        if obj.pin == None:
            obj.hasPin = False
        else:
            obj.hasPin = True
        return obj
    
    def writeImage(self, imagePath, imageNewPath):
        imageBlob = self.bucket.blob(imageNewPath) #Local Path
        imageBlob.upload_from_filename(imagePath)      
    def writeOut(self,obj):
        self.retrieveWholeDatabase()
        doc_ref = self.fireDB.collection(u'listings').document()
        imageNewPath = "itemimages/"+doc_ref.id+".jpeg"
        doc_ref.set({
            u'claimed': False,
            u'confirmed': False,
            u'descrip': obj.description,
            u'datetime': datetime.datetime.now(),
            u'lockerLocation': 'South',
            u'lockerNumber': str(obj.id),
            u'title':obj.name,
            u'filePath':imageNewPath,
            u'keyPin':0,
            u'hasPin':False,
            u'uid':"Anoynomous"
        })
        self.writeImage("/tmp/output.jpeg", imageNewPath)
    def removeObject(self, obj):
        self.retrieveWholeDatabase()
        for doc in self.docs:
            if str(doc.to_dict().get('lockerNumber')) == str(obj.id):
                self.fireDB.collection(u'listings').document(doc.id).delete()
                break#return True
        print("Removing Object",obj.id, doc.id)
        
#Help From
#https://firebase.google.com/docs/firestore/query-data/get-data
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    from firebase_admin import storage
    # Use a service account
    cred = credentials.Certificate('./restation-8e253-526f5f260257.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'restation-8e253.appspot.com'
    })
    db = DataBase()
except:
    print("Dummy Database")
    db = DataBaseTemplate()

import serial
import random
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
            print("Dummy Serial")
            self.serialWrite = lambda write :None
            self.serialQuery = lambda query :b"Yes\r\n" if input("Type something to confirm yes: ") else b"No\r\n"
    def randomLocker(self):
        return random.randint(1,10)#return locker ID
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
