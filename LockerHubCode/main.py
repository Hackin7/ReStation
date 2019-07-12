#!/usr/bin/env python

class ReuseableObject:
    id = ""
    image = "" #inBase64
    name = ""
    type = ""
    description = ""
    hasPin = True
    pin = 0
    def __init__(self):pass
    def checkPin(self,pin):
        if not havePin: return True
        elif havePin and pin == self.pin: return True
        else: return False

def imageNotAbuse(img):
    #Image is base64 Image
    #Run Command
    return True

class DataBase:
    def __init__(self):pass
    def objInDatabase(self,objID):
        output = True
        return output
    def readInObj(self,objID):
        obj = ReuseableObject()
        obj.name = "Name"
        obj.image = "ImageData"
        obj.details = "This is a dummy object"
        return obj
    def writeOut(self,obj):
        pass
db = DataBase()

class HardwareLocker:
    number = 0
    def __init__(self, number):
        self.number = number
    def open(self):
        pass
    def hasObject(self):
        return True
    def lock(self):
        pass
        
######################################################

    
import tkinter
from tkinter.constants import * 

def ShowingPage(text,backText, okText, backf, okf):
    tk = tkinter.Tk()
    frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    label = tkinter.Label(frame, text=text)
    label.pack(fill=X, expand=1)
    
    val = False
    def okPressed():
        tk.destroy()
        okf()
    ok = tkinter.Button(frame,text=okText,command=okPressed)
    ok.pack(side=RIGHT)
    
    def backmode():
        tk.destroy()
        backf()
    back = tkinter.Button(frame,text=backText,command=backmode)
    back.pack(side=LEFT)
    tk.mainloop()
   
def ShowingPageRight(text, okText, okf):
    tk = tkinter.Tk()
    frame = tkinter.Frame(tk, relief=RIDGE, borderwidth=2)
    frame.pack(fill=BOTH,expand=1)
    label = tkinter.Label(frame, text=text)
    label.pack(fill=X, expand=1)
    
    val = False
    def okPressed():
        tk.destroy()
        okf()
    ok = tkinter.Button(frame,text=okText,command=okPressed)
    ok.pack(side=RIGHT)
    
    tk.mainloop()
def mainPage():
    ShowingPage("Main Page","Put","Get",abuseDetection,selectLocker)
    
###Put Item#################################################
def abuseDetection():
    #Take photo of image to detect and avoid abuse detection
    ShowingPage("Take a Photo of the object","Exit","Take",lambda:0,lambda:0)
    img = ""
    if imageNotAbuse(img):
        putObjectDetails(img)
    else:
        print("Object not recognised")
        
    
def putObjectDetails(img):
    #Input object details
    obj = ReuseableObject()
    obj.name = input("Name:")
    obj.details = input("Details:")
    putInLocker(obj)

def putInLocker(obj):pass
###Get Item#################################################
def selectLocker():
    #Select Locker Number
    print("Select Locker")
    objID = int(input("Locker Number: "))
    while not db.objInDatabase(objID):
        print("Locker Not Found Yet")
        objID = int(input("Locker Number: "))
    getObjectDetails(objID)

def getObjectDetails(objID):
    obj = db.readInObj(objID)
    main
    showText = f"""Locker: {objID}
    Name: {obj.name}
    Type: {obj.type}
    Details: {obj.details}"""
    ShowingPage(showText,"Exit","OK",lambda:0,lambda:verification(obj))
    #Print Object Details and Stuff
    

def verification(obj):
    if obj.hasPin:
        pin = int(input("Enter PIN"))
        objPin = pin
        while pin != objPin:
            if pin == -1: return #Exit Function
            pin = int(input("Enter PIN (-1 to exit)"))
        openLocker(obj)

def openLocker(obj):
    ShowingPage("Locker","Exit","OK",lambda:0,lambda:0)
    thankYou()
    
def thankYou():
    ShowingPageRight("Thank You for Using our Services", "Ok", lambda:0)
    

def main(args):
    while True:
        mainPage()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
