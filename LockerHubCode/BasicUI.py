from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.vkeyboard import VKeyboard

from kivy.config import Config
width = 800
height = 480
Config.set('graphics', 'width', str(width))
Config.set('graphics', 'height', str(height))

transitioner=SlideTransition(direction="up")
sm = ScreenManager(transition=transitioner)
class Label(Label):
    def __init__(self,text="", **kwargs):
        super(Label, self).__init__(text = str(text),**kwargs)
class BoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(BoxLayout, self).__init__(padding=[10,10], 
                    spacing=10,**kwargs)
class VKeyboard(VKeyboard):
    def __init__(self, **kwargs):
        super(VKeyboard, self).__init__(width=width-15,**kwargs)
def popupMessage(text="An Error has occured.", title="Error", auto_dismiss=True):
    PopupMessage(text, title, auto_dismiss)
    
from kivy.uix.gridlayout import GridLayout
def objectDisplayLayout(obj, booked=True):
        rightcol = 0.25
        leftcol = 1-rightcol
        
        objOut = GridLayout(cols=2, padding=[10,10])
        def templateLabel(text,x=1,y=0.5):
            l = Label(text=text, size_hint_x=x,size_hint_y=y, font_size="20dp")
            l.text_size = (int(width*x),l.size[1])
            return l
        objOut.add_widget(templateLabel('Object ID Given:',rightcol))
        objOut.add_widget(templateLabel(obj.id,leftcol))
        objOut.add_widget(templateLabel('Name:',rightcol))
        objOut.add_widget(templateLabel(obj.name,leftcol))
        objOut.add_widget(templateLabel('Description:',rightcol,2.0))
        objOut.add_widget(templateLabel(obj.description,leftcol,2.0))
        if booked:
            objOut.add_widget(templateLabel('Booked:',rightcol))
            objOut.add_widget(templateLabel(str(obj.hasPin),leftcol))       
        return objOut
        
class PopupMessage:
    def __init__(self,text="An Error has occured.", title="Error", auto_dismiss=True):
        self.content = Label(text=text,font_size="20dp")
        self.popup = Popup(title=title, content=self.content, 
                            size_hint=(None, None),size=(400, 400),
                            auto_dismiss=auto_dismiss)
        # open the popup
        self.popup.open()
    def dismiss(self):
        self.popup.dismiss()
import threading
def loading(run, args=()):
    def toRun():
        run()
        load.dismiss()
    load = PopupMessage("Loading...", "Loading", False)
    x = threading.Thread(target=toRun)
    x.start()
def confirmPopup(text="Are you sure?", title="Error", leftScreen="",rightScreen=""):
    main = Label(text=text,font_size="20dp")
    
    bottom = BottomBar("No", "Yes", leftScreen, rightScreen)
    
    content = BoxLayout(orientation='vertical')
    content.add_widget(main)
    content.add_widget(bottom.main)
    popup = Popup(title=title, content=content, 
    size_hint=(None, None),size=(400, 400))
    bottom.leftButton.bind(on_press=popup.dismiss)
    bottom.rightButton.bind(on_press=popup.dismiss)
    # open the popup
    popup.open()
class MyButton(Button):
    def __init__(self, page="", function=lambda:None, **kwargs):
        self.page = page
        self.function = function
        super(MyButton, self).__init__(size_hint=(.7, .7),
                        font_size="20dp", **kwargs)
    def on_press(self):
        self.function()
        if self.page != "":
            sm.current = self.page

def bottomBar(left, right, leftScreen, rightScreen, 
              leftFunction=lambda:None, rightFunction=lambda:None):
    bottom = BottomBar(left, right, leftScreen, rightScreen, leftFunction, rightFunction)
    return bottom.main

class BottomBar:
    def __init__(self,left, right, leftScreen, rightScreen, 
              leftFunction=lambda:None, rightFunction=lambda:None):
        self.left = left
        self.right = right
        self.leftScreen= leftScreen
        self.rightScreen = rightScreen
        self.leftFunction = leftFunction
        self.rightFunction = rightFunction
        self.generateBar()
    def generateBar(self):
        self.leftButton = MyButton(text=self.left, 
                              page=self.leftScreen, 
                              function=self.leftFunction)
        self.rightButton = MyButton(text=self.right, 
                               page=self.rightScreen, 
                               function=self.rightFunction)
        self.main = BoxLayout()
        self.main.add_widget(self.leftButton)
        self.main.add_widget(self.rightButton)
        self.main.size_hint = (1.0,0.75)
        
class ShowScreen(Screen):    
    def __init__(self, main="Hello",\
                left = "Back",right="Ok",
                leftScreen="",rightScreen="",
                leftFunction=lambda:None, rightFunction=lambda:None,
                **kwargs):
        super(ShowScreen, self).__init__(**kwargs) 
          
        self.mainText = main
        self.leftText = left
        self.rightText= right
        self.leftScreen = leftScreen
        self.rightScreen = rightScreen
        self.leftFunction = lambda:None
        self.rightFunction = lambda:None
        
        self.generateLayout()
    def update(self, obj):
        pass
    def generateLayout(self):
        r1 = Label(text=self.mainText, markup=True)
        #r1.font_size = '50dp'
        r2 = bottomBar(self.leftText, self.rightText, 
                       self.leftScreen, self.rightScreen, 
                       self.leftFunction, self.rightFunction)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(r1)
        layout.add_widget(r2)
        self.clear_widgets()
        self.add_widget(layout)            

class PinEntry(Screen):
    text=""
    toScreen=""
    def __init__(self, text="Enter Pin:",toScreen="",**kwargs):
        super(PinEntry, self).__init__(**kwargs)
        self.text=text
        self.toScreen = toScreen
        self.generateLayout()
    def buttonFunction(self):
        pin = self.pinInput.text
        if len(pin) == 0:
            popupMessage("No Pin Entered!")
        elif self.toScreen != "":
            sm.get_screen(self.toScreen).update(pin)
            sm.current = self.toScreen
    def key_down(self, keyboard, keycode, text, modifiers):
        """ The callback function that catches keyboard events. """
        if text != None:
            self.pinInput.text += text
        if keycode == "backspace":
            self.pinInput.text = self.pinInput.text[:-1]
    def generateLayout(self):
        r1 = Label(text=self.text,size_hint=(1.0,0.5))
        r1.font_size = '30dp'
        self.pinInput = TextInput(multiline=False,input_filter= 'float',
                                    size_hint=(1.0,0.5))
        key = VKeyboard()
        key.bind(on_key_down=self.key_down)
        nav = bottomBar("Back", "Ok", 
                       "menu", "", 
                       lambda:None, self.buttonFunction)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(r1)
        layout.add_widget(self.pinInput)
        layout.add_widget(key)
        layout.add_widget(nav)
        self.add_widget(layout) 
