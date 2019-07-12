# -*- coding: utf-8 -*-

from BasicUI import *
from kivy.uix.gridlayout import GridLayout
import Interface as intf
import sys
sys.path.append('./ImageRecognition')

###Put##################################################################
class CheckImageNotAbuse(ShowScreen):
    obj = intf.ReuseableObject()
    def update(self,obj):
        self.obj = obj
        obj.toPut = True
    def buttonRight(self):
        intf.im.check()
        self.obj.image = intf.im.image
        if intf.im.isAbuse:
            popupMessage("This Object is not accpetable\nfor the time being.\nSorry for the inconvenience")
        else:
            sm.get_screen(self.toScreen).update(self.obj)
            sm.current=self.toScreen
            
    def __init__(self,toScreen="unlock", **kwargs):
        super(CheckImageNotAbuse, self).__init__(**kwargs)
        self.toScreen = toScreen
        self.rightScreen = ""
        self.rightFunction = self.buttonRight
        self.generateLayout()
    '''
    def generateLayout(self):
        r1 = Label(text=self.mainText)
        cam = Camera(play=True)
        r2 = bottomBar(self.leftText, self.rightText, 
                       self.leftScreen, self.rightScreen, 
                       self.leftFunction, self.rightFunction)
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(r1)
        layout.add_widget(cam)
        layout.add_widget(r2)
        self.clear_widgets()
        self.add_widget(layout)   
    '''
        
class PutObjectDetails(Screen):
    obj = intf.ReuseableObject()
    inputMode = 0
    def __init__(self, toScreen="put2", backScreen="menu",**kwargs):
        super(PutObjectDetails, self).__init__(**kwargs) 
        self.toScreen = toScreen
        self.backScreen = backScreen
        self.generateLayout()
        
    def update(self, obj=intf.ReuseableObject()):
        self.obj = obj
        self.generateLayout()
        
    def on_focus(self, inputMode):
        def switchArea(instance, value):
            if value:
            #    print('User focused', instance)   
                self.inputMode = inputMode             
            #else:
            #    print('User defocused', instance)
        return switchArea
    
    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard events. """
        if text != None:
            if self.inputMode == 0:
                self.objName.text += text
            elif self.inputMode == 1:
                self.objDetails.text += text
        if keycode == "backspace":
            if self.inputMode == 0:
                self.objName.text = self.objName.text[:-1]
            elif self.inputMode == 1:
                self.objDetails.text = self.objDetails.text[:-1]
    def generateLayout(self):
        def sendData():
            self.obj.name = self.objName.text
            self.obj.description = self.objDetails.text
            sm.get_screen(self.toScreen).update(self.obj)
            
        self.objName = TextInput()
        self.objDetails = TextInput()
        
        self.objName.bind(focus=self.on_focus(0))
        self.objDetails.bind(focus=self.on_focus(1))
        
        inputIn = GridLayout(cols=2)
        inputIn.add_widget(Label(text='Name:', size_hint_x=0.25, font_size="20dp"))
        inputIn.add_widget(self.objName)
        inputIn.add_widget(Label(text='Description:', size_hint_x=0.25, font_size="20dp"))
        inputIn.add_widget(self.objDetails)
        
        key = VKeyboard()
        key.bind(on_key_down=self.key_down)
        
        bottom = bottomBar("Back", "Ok", self.backScreen,self.toScreen, lambda:None, sendData)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(inputIn)
        layout.add_widget(key)
        layout.add_widget(bottom)
        self.clear_widgets()
        self.add_widget(layout)

class ConfirmObjDetails(ShowScreen):
    obj = intf.ReuseableObject()
    def __init__(self, **kwargs):
        super(ConfirmObjDetails, self).__init__(**kwargs)
    def update(self,obj):
        self.obj = obj
        self.obj.id = intf.hl.randomLocker()
        details = f"""
        Confirm Object Details:
        Object ID:{self.obj.id}
        Name: {self.obj.name}
        Description: {self.obj.description}
        """
        def passObject():
            sm.get_screen(self.rightScreen).update(self.obj)
            
        self.mainText = details
        self.rightFunction = passObject
        self.generateLayout()

###PutKey###############################################################
class PutKey(PinEntry):
    def buttonFunction(self):
        ID = self.pinInput.text
        if len(ID) == 0:
            popupMessage("No Registration ID Entered!")
        elif intf.db.registrationInDatabase(ID) and self.toScreen != "":
            self.obj = intf.db.getRegistration(ID)
            sm.get_screen(self.toScreen).update(self.obj)
            sm.current = self.toScreen
        else:
            popupMessage("No Such Registration ID Exists!")
            
###Get##################################################################
class SelectLocker(PinEntry):
    def buttonFunction(self):
        ID = self.pinInput.text
        if len(ID) == 0:
            popupMessage("No Locker ID Entered!")
        elif intf.db.objInDatabase(ID) and self.toScreen != "":
            obj = intf.db.readInObj(ID)
            obj.toPut = False
            sm.get_screen(self.toScreen).update(obj)
            sm.current = self.toScreen
        else:
            popupMessage("No Such Locker ID Exists!")
            
class ShowObjectDetails(ShowScreen):
    obj = intf.ReuseableObject()
    def __init__(self, **kwargs):
        super(ShowObjectDetails, self).__init__(**kwargs)
    def update(self,obj):
        self.obj = obj
        details = f"""
        Object ID:{obj.id}
        Name: {self.obj.name}
        Description: {self.obj.description}
        Booked: {self.obj.hasPin}"""
        
        if self.obj.hasPin:
            passScreen = "get3"
        else:
            passScreen = "unlock"
        def passObject():
            sm.get_screen("unlock").update(self.obj)
            if self.obj.hasPin:
                sm.get_screen("get3").update(self.obj)
        self.mainText = details
        self.rightScreen = passScreen
        self.rightFunction = passObject
        self.generateLayout()
    def objectDisplayLayout(self, obj):
        objOut = GridLayout(cols=2)
        objOut.add_widget(Label(text='Object ID:', size_hint_x=0.25, font_size="20dp"))
        objOut.add_widget(Label(text=obj.id,halign="left"))
        objOut.add_widget(Label(text='Name:', size_hint_x=0.25, font_size="20dp"))
        objOut.add_widget(Label(text=obj.name,halign="left"))
        objOut.add_widget(Label(text='Description:', size_hint_x=0.25,size_hint_y=2.0, font_size="20dp"))
        objOut.add_widget(Label(text=obj.description,halign="left"))
        objOut.add_widget(Label(text='Booked:', size_hint_x=0.25, font_size="20dp"))
        objOut.add_widget(Label(text=str(obj.hasPin),halign="left"))
        return objOut
        
    def generateLayout(self):
        r1 = self.objectDisplayLayout(self.obj)
        #r1.font_size = '50dp'
        r2 = bottomBar(self.leftText, self.rightText, 
                       self.leftScreen, self.rightScreen, 
                       self.leftFunction, self.rightFunction)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(r1)
        layout.add_widget(r2)
        self.clear_widgets()
        self.add_widget(layout) 
                        
class Verification(PinEntry):
    toScreen = "unlock"
    text="Verify Code"
    obj = intf.ReuseableObject()
    def __init__(self, **kwargs):
        super(Verification, self).__init__(text = self.text,
                                           toScreen=self.toScreen,
                                           **kwargs)
    def buttonFunction(self):
        pin = self.pinInput.text
        if len(pin) == 0:
            popupMessage("No Pin Entered!")
        elif pin != self.obj.pin:
            popupMessage("Pin Incorrect!")
        elif self.toScreen != "":
            #sm.get_screen(self.toScreen).update(self.obj, True)
            sm.current = self.toScreen
    def update(self, obj):
        self.obj = obj

###Common###############################################################        
class Unlocking(ShowScreen):
    obj = intf.ReuseableObject()
    def buttonRight(self):
        if self.toPut and intf.hl.hasObject(self.obj):
            intf.db.writeOut(self.obj)
            sm.get_screen(self.toScreen).update(self.obj)
            sm.current=self.toScreen
        elif not self.toPut and not intf.hl.hasObject(self.obj):
            intf.db.removeObject(self.obj)
            sm.get_screen(self.toScreen).update(self.obj)
            sm.current=self.toScreen
        else:
            popupMessage("There were no changes to the locker!\nPress Back to quit.")
            
    def buttonLeft(self):
        confirmPopup("Are you sure you go back to main menu", 
         rightScreen=self.toScreen)

    def update(self,obj):
        self.obj = obj
        self.toPut = self.obj.toPut
        self.leftFunction=self.buttonLeft
        self.rightFunction=self.buttonRight
        self.mainText = f"[size=40dp]Locker {obj.id} is unlocked[/size]"
        self.generateLayout()
        intf.hl.unlock()
        
    def __init__(self, toScreen="",**kwargs):
        super(Unlocking, self).__init__(**kwargs)
        self.toScreen = toScreen

class CloseDoor(Screen):
    obj = intf.ReuseableObject()
    def buttonFunction(self):
        if intf.hl.doorClosed():
            sm.current=self.toScreen
            intf.hl.lock()
        else:
            popupMessage("The door needs to be closed!\n")
            
    def update(self,obj):
        self.obj = obj
        self.toPut = self.obj.toPut
        self.mainText = f"Please Close {obj.id}"
        self.generateLayout()
        
    def __init__(self,main="Please Close the Door",toScreen="menu",**kwargs):
        super(CloseDoor, self).__init__(**kwargs)
        self.mainText = main
        self.toScreen = toScreen
        self.generateLayout()
        
    def generateLayout(self):
        r1 = Label(text=self.mainText)
        r2 = MyButton(text="Ok", 
                        page="", 
                    function=self.buttonFunction)
        r2.size_hint = (1.0, 0.5)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(r1)
        layout.add_widget(r2)
        self.clear_widgets()
        self.add_widget(layout)     
    
mainScreen = ShowScreen(name='menu', 
                        main="[size=50dp]Welcome to the\nReuse Station[/size]",
                        left="Put Item",right="Get Item",
                        leftScreen="put0",rightScreen="get1")
put0 = ShowScreen(name='put0', main="[size=40dp]Have you already made\n a listing online?[/size]",
                        left="No",right="Yes",
                        leftScreen="put1",rightScreen="putkey")

put1 = PutObjectDetails(name='put1')
putkey = PutKey(name="putkey", toScreen="put2", text="Enter Registration ID:")
put2 = ConfirmObjDetails(name='put2', leftScreen="menu", rightScreen="put3")
put3 = CheckImageNotAbuse(name='put3', main="Take a Picture of the Item",
                        left="Back",right="Ok",
                        leftScreen="menu",rightScreen="put3")

get1 = SelectLocker(name="get1", toScreen="get2", text="Enter Locker ID:")
get2 = ShowObjectDetails(name="get2", leftScreen="menu")
get3 = Verification(name="get3")
unlocked = Unlocking(name='unlock',toScreen="close",
                        left="Back",right="Done?")
close = CloseDoor(name="close", toScreen="menu")

# Create the screen manager
sm.add_widget(mainScreen)
sm.add_widget(put0)
sm.add_widget(putkey)
sm.add_widget(put1)
sm.add_widget(put2)
sm.add_widget(put3)
sm.add_widget(get1)
sm.add_widget(get2)
sm.add_widget(get3)
sm.add_widget(unlocked)
sm.add_widget(close)

class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()
