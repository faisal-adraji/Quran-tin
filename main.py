'''
author  :   Faisal Adraji
email   :   faisal.adraji@gmail.com
version :   0.0
start   :   12-2017
kivy.require("1.9.0")
'''


#import sys
#sys.path.append("/storage/emulated/0/kivy/Tin")

# import threading
import kivy
kivy.require("1.9.0")

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
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp, dp

# from tinsv import MyScrollView


FIRST_PAGE= 0
LAST_PAGE= 603
SPEED_STEP= 1000
INITIAL_SPEED= 10000
INITIAL_SIZE= 500


from kivy.lang import Builder

Builder.load_string('''
<Tin>:

    MyScrollView:
        id: sv
        BoxLayout:
            id: box
            size_hint_y: 500
            orientation: 'vertical'
            #on_touch_down: root.hide_menu(menu)

    Image:
        id: lbl_bg
        size_hint: (1, .05)
        pos_hint: {'x':.0, 'y':.0}
        color: .4, .4, .4, 1
        allow_stretch: True

    Label:
        id: lbl
        text: 'void'
        markup: True
        size_hint: (.2, .05)
        pos_hint: {'x':.4, 'y':.0}
        # size_hint: (.2, .06)
        #pos: (200,0)


    # Button:
    #     id: menu_btn
    #     size_hint: (.05, .05)
    #     pos_hint: {'x':.4725, 'y':.93}
    #     on_press: root.show_menu(menu)
    Button:
        id: menu_btn_1
        size_hint: (1, .1)
        pos_hint: {'x':.0, 'y':.95}
        on_press: root.hide_menu(menu) if root.menu else root.show_menu(menu) 


    

# menu



    FloatLayout:
        id: menu
        text: 'menu'
        # position and size to the parent, root in this case
        size_hint: (.90, .40)
        pos_hint: {'x':.05, 'y':.05}
        orientation: 'vertical'
        opacity: 1 if root.menu else 0

        Image:
            id: menu_bg
            size: menu.size
            pos: menu.pos
            #source: 'free.png'
            color: .2, .2, .2, 1
            allow_stretch: True


        Label:
            text: 'MENU'
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.87}
            font_size: 30
            color: 1, 1, 0, 1
            
        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.7}

            Button:
                id: autoscroll_btn
                text: 'autoscroll'
                on_press: root.autoscroll(sv, box, autoscroll_btn)

                
        Label:
            text: 'size'
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.55}
            font_size: 20

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.45}

            Button:
                id: siz_dwn_btn
                text: 'down'
                # size_hint: (.15, .05)
                # pos_hint: {'x':.2, 'y':.8}
                on_press: root.siz_dwn(box)

            MyLabel:
                id: lbl_viw_siz
                text: 'void'
                markup: True
                # size_hint: (.25, .06)
                # pos: (0,440)
                
            Button:
                id: siz_up_btn
                text: 'up'
                #size_hint: (.15, .05)
                #pos_hint: {'x':.8, 'y':.8}
                on_press: root.siz_up(box)

        Label:
            text: 'seconds per page'
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.3}
            font_size: 20

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.2}

            Button:
                id: spd_dwn_btn
                text: '-'
                on_press: root.spd_dwn(sv, box)
            MyLabel:
                id: lbl_scrl_spd
                text: 'void'
                markup: True
            Button:
                id: spd_up_btn
                text: '+'
                on_press: root.spd_up(sv, box)

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.05}
            #orientation: 'vertical'

            TextInput:
                id: ti
                text: '1'
                multiline: False
                on_text_validate: root.goto_page(sv, box, ti)
                # height= '32dp'
            Button:
                id: goto_page_btn
                text: 'goto'
                on_press: root.goto_page(sv, box, ti)

    ''')


class MyScrollView(ScrollView):
    spd = 10000
    def scroll_to(self, widget, padding=10, animate=True, d=200):

        if not self.parent:
            return

        # if _viewport is layout and has pending operation, reschedule
        if hasattr(self._viewport, 'do_layout'):
            if self._viewport._trigger_layout.is_triggered:
                Clock.schedule_once(
                     lambda *dt: self.scroll_to(widget, padding, animate))
                return

        if isinstance(padding, (int, float)):
            padding = (padding, padding)

        pos = self.parent.to_widget(*widget.to_window(*widget.pos))
        cor = self.parent.to_widget(*widget.to_window(widget.right,
                                                      widget.top))

        dx = dy = 0

        if pos[1] < self.y:
            dy = self.y - pos[1] + dp(padding[1])
        elif cor[1] > self.top:
            dy = self.top - cor[1] - dp(padding[1])

        if pos[0] < self.x:
            dx = self.x - pos[0] + dp(padding[0])
        elif cor[0] > self.right:
            dx = self.right - cor[0] - dp(padding[0])

        dsx, dsy = self.convert_distance_to_scroll(dx, dy)
        sxp = min(1, max(0, self.scroll_x - dsx))
        syp = min(1, max(0, self.scroll_y - dsy))

        if animate:
            if animate is True:
                animate = {'d': d, 't': 'linear'} #0.2
            Animation.stop_all(self, 'scroll_x', 'scroll_y')
            Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp




class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.5, .5, .5, 1)
            Rectangle(pos=self.pos, size=self.size)






class Tin(FloatLayout):


    scrolling = 0
    menu = 1
    step = 1
    global curt_page
    
    #ti = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Tin, self).__init__(**kwargs)
        

    def update(self, dt):
        bl = self.ids.box
        sv = self.ids.sv
        lbl_spd = self.ids.lbl_scrl_spd
        lbl_siz = self.ids.lbl_viw_siz
        lbl = self.ids.lbl


        self.curt_page = int(((1-sv.scroll_y)*(LAST_PAGE))+1.5)

        #many calculation in the next line of code : 
        #1-sv.scroll_y because scroll_y is reversed
        #LAST_PAGE-1 
        #+1.5 is for updating page number at the midle of page 
        lbl.text = str(self.curt_page)
        lbl_spd.text = str(sv.spd)
        lbl_siz.text = str(bl.size_hint[1])

        #he next linesare for manual page's texture buffer handler

        mid= int(((1-sv.scroll_y)*(LAST_PAGE)))

        beg= mid-3
        end= mid+3
        if beg < 0 : beg = 0
        if end > LAST_PAGE : end = LAST_PAGE

        for i in range(0, beg+1):
            bl.children[LAST_PAGE- i].source = 'free.jpg'

        for i in range(end, LAST_PAGE+1):
            bl.children[LAST_PAGE- i].source = 'free.jpg'

        for i in range(beg, end+1):
            strg= ('pages/page_' + str(i) + '.jpg')
            bl.children[LAST_PAGE- i].source = strg



    #functions for buttons

    def autoscroll(self, sv, box, autoscroll_btn):
        if not self.scrolling :
            sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
            self.scrolling = 1
            autoscroll_btn.text = 'stop'
        else :
            sv.scroll_to(box.children[LAST_PAGE - self.curt_page +1], d= 0.2 )
            self.scrolling = 0
            autoscroll_btn
            autoscroll_btn.text = 'autoscroll'

    def spd_dwn(self, sv, box):
            sv.spd = sv.spd - self.step
            if self.scrolling:
                sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
            # print sv.spd * (LAST_PAGE - self.curt_page)
            # print LAST_PAGE
            # print self.curt_page
            # print sv.spd
            #popup = Popup(title='im scrolling', size_hint=(0.5, 0.5))
            #popup.open()
        
    def spd_up(self, sv, box):
        sv.spd = sv.spd + self.step
        if self.scrolling:
            sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
    
    def goto_page(self, sv, box, ti):
        sv.scroll_to(box.children[LAST_PAGE - int(ti.text) +1], d=0.2)
        self.scrolling = 0
    
    def siz_up(self, box):
        box.size_hint[1]+= 10
    
    def siz_dwn(self, box):
        box.size_hint[1]-= 10

    def hide_menu(self, menu):
        if self.menu:
            menu.opacity = 0
            menu.size_hint_x = .0
            self.menu = 0

    def show_menu(self, menu):
        if not self.menu:
            menu.opacity = 1
            menu.size_hint_x = .9
            self.menu = 1

class TinApp(App):

    global Window
    global wdg


    def build(self):
        #str(int(5000)        
        #Window.clearcolor = (.95,.95,.95,1)
        #Window.size = (1024, 768)
        #Window.set_title('TinApp')
        self.title = 'Tin'
        self.icon = 'tin.png'
        self.wdg = Tin(size=(400, 400))
        main_wdg = self.wdg

        #finaly found the way for calling object from kv file
        sv  = main_wdg.ids.sv
        box = main_wdg.ids.box
        ti  = main_wdg.ids.ti
         
        lbl = main_wdg.ids.lbl    
        lbl_scrl_spd = main_wdg.ids.lbl_scrl_spd
        lbl_viw_siz = main_wdg.ids.lbl_viw_siz




        #restore last session
        f = open("save.dat")
        self.curt_page = f.readline()
        box.size_hint[1] = int(f.readline())
        sv.spd = int(f.readline())
        f.close()
        
        
        
    # initializing graphic objects
        
        #fill boxlayout with pages
        # for i in reversed(range(FIRST_PAGE, LAST_PAGE)):
        for i in range(FIRST_PAGE, LAST_PAGE+1):
            #strg =('pages/page_' + str(i) + '.jpg')
            img = Image(source= 'free.jpg')
            box.add_widget(img, len(box.children))


        sv.scroll_y = 1 - float(self.curt_page)/604
        Clock.schedule_interval(main_wdg.update, 1.0 / 60.0)
        return main_wdg

    def on_stop(self):
        curt_page = self.wdg.curt_page
        size = self.wdg.ids.box.size_hint[1]
        spd = self.wdg.ids.sv.spd
        f = open("save.dat", "w")
        f.write( str(curt_page -1) + '\n')  
        f.write( str(size) + '\n')
        f.write( str(spd) )
        # f.write(  str((1 - SCROLL_Y/1)*604)  )  
        f.close()



if __name__ == '__main__':
    TinApp().run()