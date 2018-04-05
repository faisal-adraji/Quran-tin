'''
author  :   Faisal Adraji
email   :   faisal.adraji@gmail.com
start   :   12-2017
kivy.require("1.9.0")
'''

FIRST_PAGE = 0
LAST_PAGE = 603
SIZE_STEP = 100
SPEED_STEP = 1000
INITIAL_SPEED =10000
INITIAL_SIZE =500


#import sys
#sys.path.append("/storage/emulated/0/kivy/tibib")

import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from Sv import MyScrollView

from kivy.lang import Builder

Builder.load_string('''
#:import Factory kivy.factory.Factory
<Tin>:
    MyScrollView:
        id: sv
        BoxLayout:
            id: box
            size_hint_y: 500
            orientation: 'vertical'
    MyLabel:
        id: lbl
        text: 'void'
        markup: True
        size_hint: (.2, .06)
        pos: (200,50)

    Button:
        id: autoscroll_btn
        text: 'autoscroll'
        size_hint: (.15, .05)
        pos_hint: {'x':.425, 'y':.95}
        on_press: root.autoscroll(sv, box)

''')

class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.5, .5, .5, 1)
            Rectangle(pos=self.pos, size=self.size)






class Tin(FloatLayout):
    
    #ti = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Tin, self).__init__(**kwargs)
        

    def update(self, dt):
        bl = self.ids.box
        sv = self.ids.sv
        lbl_spd = self.children[0]
        lbl_siz = self.children[1]
        lbl = self.ids.lbl

        #many calculation in the next line of code : 
        #1-sv.scroll_y because scroll_y is reversed
        #LAST_PAGE-1 
        #+1.5 is for updating page number at the midle of page 
        lbl.text = 'page : ' + str(int(((1-sv.scroll_y)*(LAST_PAGE-1))+1.5))
        lbl_spd.text = 'speed : ' + str(sv.spd/1000)
        lbl_siz.text = 'size : ' + str(bl.size_hint[1])

        #he next linesare for manual page's texture buffer handler

        mid= int(((1-sv.scroll_y)*(LAST_PAGE-1)))

        beg= mid-3
        end= mid+3
        if beg < 0 : beg = 0
        if end > LAST_PAGE : end = LAST_PAGE


        for i in range(beg, end):
            strg= ('pages/page_' + str(i) + '.jpg')
            bl.children[LAST_PAGE-1- i].source = strg


        for i in range(0, beg):
            bl.children[LAST_PAGE-1- i].source = 'free.jpg'

        for i in range(end, LAST_PAGE):
            bl.children[LAST_PAGE-1- i].source = 'free.jpg'

    def autoscroll(self, sv, box):
        sv.scroll_to(box.children[0], d= sv.spd)
        print 'this is scroll'
        #self.scrolling = 1

class TinApp(App):

    scrolling = 0
    step = 100
    global Window


    def build(self):
        #str(int(5000)        
        #Window.clearcolor = (.95,.95,.95,1)
        #Window.size = (1024, 768)
        #Window.set_title('TinApp')
        #self.title = 'Tin'
        app = Tin(size=(400, 400))

        #finaly found the way for calling obect from kv file
        sv  = app.ids.sv
        box = app.ids.box
        ti = TextInput(text= '1',size_hint=(.15, .05),pos_hint={'x':.5, 'y':.0}, multiline=False) # height= '32dp'
         
        lbl = app.ids.lbl    
        lbl_scrl_spd = MyLabel(text= 'void', markup= True, size_hint=(.25, .06),pos= (400,50))      
        lbl_viw_siz = MyLabel(text= 'void', markup= True, size_hint=(.25, .06),pos= (0,50))      

    #functions for buttons
        
        def spd_dwn(instance):
            sv.spd = sv.spd + self.step
            if self.scrolling:
                sv.scroll_to(box.children[0], d= sv.spd)
            #popup = Popup(title='im scrolling', size_hint=(0.5, 0.5))
            #popup.open()
        
        def spd_up(instance):
            sv.spd = sv.spd - self.step
            if self.scrolling:
                sv.scroll_to(box.children[0], d= sv.spd)
        
        def goto_page(instance):
            sv.scroll_to(box.children[LAST_PAGE - int(ti.text)], d=0.2)
        
        def siz_up(instance):
            box.size_hint[1]+= 10
        
        def siz_dwn(instance):
            box.size_hint[1]-= 10
        
    # initializing graphic objects
        
        spd_dwn_btn = Button(text= 'spd-', size_hint=(.15, .05),pos_hint={'x':.7, 'y':.95})
        spd_dwn_btn.bind(on_press=spd_dwn)

        spd_up_btn = Button(text= 'spd+', size_hint=(.15, .05),pos_hint={'x':.15, 'y':.95})
        spd_up_btn.bind(on_press=spd_up)
        
        goto_page_btn = Button(text= 'goto', size_hint=(.15, .05),pos_hint={'x':.7, 'y':.0})
        goto_page_btn.bind(on_press=goto_page)
        
        ti.bind(on_text_validate=goto_page)
        
        siz_dwn_btn = Button(text= 'down', size_hint=(.15, .05),pos_hint={'x':.1, 'y':.0})
        siz_dwn_btn.bind(on_press=siz_dwn)
        
        siz_up_btn = Button(text= 'up', size_hint=(.15, .05),pos_hint={'x':.3, 'y':.0})
        siz_up_btn.bind(on_press=siz_up)
        
        #fill boxlayout with pages
        for i in reversed(range(FIRST_PAGE, LAST_PAGE)):
            strg=('pages/page_' + str(i) + '.jpg')
            img = Image(source= 'free.jpg')
            box.add_widget(img, len(box.children))
       
        #fill thee scrollview with the unique boxlayout witch contain all pages
        #app.add_widget(autoscroll_btn)
        app.add_widget(spd_dwn_btn)
        app.add_widget(spd_up_btn)
        app.add_widget(goto_page_btn)
        app.add_widget(siz_dwn_btn)
        app.add_widget(siz_up_btn)
        app.add_widget(ti)
        app.add_widget(lbl_scrl_spd)
        app.add_widget(lbl_viw_siz)
        #app.add_widget(lbl)

        Clock.schedule_interval(app.update, 1.0 / 30.0)
        
        return app


if __name__ == '__main__':
    TinApp().run()
