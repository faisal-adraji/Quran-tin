'''
author  :   Faisal Adraji
email   :   faisal.adraji@gmail.com
version :   0.0
start   :   12-2017
kivy.require("1.9.0")
'''


#import sys
#sys.path.append("/storage/emulated/0/kivy/Tin")

import threading
import kivy
kivy.require("1.9.0")

#necesary for utf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# from kivy import Config
# Config.set('graphics', 'multisamples', 0)

# from jnius import autoclass

# # all this to prevent device sleep
# activity = autoclass('org.renpy.android.PythonActivity')
# # PythonActivity = autoclass('org.renpy.android.PythonActivity')
# v = autoclass('android.view.View')
# params = autoclass('android.view.WindowManager$LayoutParams')
# from android.runnable import run_on_ui_thread

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from kivy.animation import Animation, AnimationTransition
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp, dp
from kivy.compat import string_types
from kivy.weakproxy import WeakProxy


# from tinsv import MyScrollView


FIRST_PAGE= 0
LAST_PAGE= 603
SPEED_STEP= 1000
INITIAL_SPEED= 10000
INITIAL_SIZE= 500
ANIM_STEP= 1/10.0

scrolling = 0

from kivy.lang import Builder

Builder.load_string('''
<Tin>:

    TinScrollView:
        id: sv
        pos: (0,0)
        BoxLayout:
            id: box
            size_hint_x: 1
            size_hint_y: 500
            orientation: 'vertical'
            #on_touch_down: root.hide_kb()



#page bar

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

    Button:
        id: rev_btn
        text: '<='
        size_hint: (.1, .05)
        pos_hint: {'x':.0, 'y':.0}
        on_press: root.reverse(sv, box)


#head button with progress bar inside him


    # Button:
    #     id: menu_btn
    #     size_hint: (.05, .05)
    #     pos_hint: {'x':.4725, 'y':.93}
    #     on_press: root.show_menu()
    Button:
        id: menu_btn
        size_hint: (1, .1)
        pos_hint: {'x':.0, 'y':.93}
        on_press: root.hide_menu() if root.ismenu else root.show_menu() 
    ProgressBar:
        id: pb
        size_hint: (1, .04)
        pos_hint: {'x':.0, 'y':.93}
        height: '92dp'
        value: 0
    Label:
        id: lbl_hizb_bar
        font_name: 'arial.ttf'
        text: u'\ufe8f\ufeaf\ufea3'
        size_hint: (.8 , .1)
        pos_hint: {'x':.2, 'y':.935}


    

# menu



    FloatLayout:
        id: menu
        text: 'menu'
        # position and size to the parent, root in this case
        size_hint: (.90, .50)
        pos_hint: {'x':.05, 'y':.05}
        orientation: 'vertical'
        opacity: 1 if root.ismenu else 0

        Image:
            id: menu_bg
            size: menu.size
            pos: menu.pos
            #source: 'free.png'
            color: .2, .2, .2, 1
            allow_stretch: True

        Button:
            id: close_menu
            text: 'X'
            size_hint: (.1, .1)
            pos_hint: {'x':.9, 'y':.9}
            on_press: root.hide_menu()
        Button:
            id: show_help
            text: '?'
            size_hint: (.1, .1)
            pos_hint: {'x':0, 'y':.9}
            on_press: root.show_lgd()

        Label:
            id: title
            font_name: 'arial.ttf'
            text: u'\ufe94\ufee4\ufe8b\ufe8e\ufed8\ufedf\ufe8d' #utf code mean menu in arabic
            size_hint: (.66, .2)
            pos_hint: {'x':.17, 'y':.8}
            #font_size: 30
            color: 1, 1, 0, 1
            
        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.7}

            Button:
                id: autoscroll_btn
                font_name: 'arial.ttf'
                text: u'\ufe93\ufe83\ufead\ufed8\ufedf\ufe8d' #utf code means read in arabic
                on_press: root.autoscroll(sv, box, autoscroll_btn)

                
        Label:
            font_name: 'arial.ttf'
            text: u'\ufe94\ufea4\ufed4\ufebc\ufedf\ufe8d\u0020\ufee1\ufea0\ufea3' #utf code means size in arabic
            size_hint: (.66, .2)
            pos_hint: {'x':.17, 'y':.55}
            #font_size: 20

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.45}

            Button:
                id: siz_dwn_btn
                font_name: 'arial.ttf'
                text: u'\ufead\ufef4\ufed0\ufebc\ufe97' #utf code means size down in arabic
                # size_hint: (.15, .05)
                # pos_hint: {'x':.2, 'y':.8}
                on_press: root.siz_dwn(box)

            TinLabel:
                id: lbl_viw_siz
                text: 'void'
                markup: True
                # size_hint: (.25, .06)
                # pos: (0,440)
                
            Button:
                id: siz_up_btn
                font_name: 'arial.ttf'
                text: u'\ufead\ufef4\ufe92\ufedc\ufe97' #utf code means size up in arabic
                #size_hint: (.15, .05)
                #pos_hint: {'x':.8, 'y':.8}
                on_press: root.siz_up(box)

        Label:
            font_name: 'arial.ttf'
            text: u'\ufe94\ufea4\ufed4\ufebb\u0020\ufedd\ufedc\ufedf\ufef2\ufee7\
\ufe8d\ufeed\ufe9c\ufedf\ufe8d\u0020\ufea9\ufea9\ufecb' #utf code means second per page in arabic
            size_hint: (.66, .2)
            pos_hint: {'x':.17, 'y':.3}
            #font_size: 20

        BoxLayout:
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.2}

            Button:
                id: spd_dwn_btn
                text: '-'
                on_touch_down: root.isspd_dwn = 1
                on_touch_up: root.isspd_dwn = 0
            TinLabel:
                id: lbl_scrl_spd
                text: ''
                markup: True
            Button:
                id: spd_up_btn
                text: '+'
                on_touch_down: root.isspd_up = 1
                on_touch_up: root.isspd_up = 0

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.66, .1)
            pos_hint: {'x':.17, 'y':.05}
            #orientation: 'vertical'

            Button:
                id: open_kb
                font_name: 'arial.ttf'
                text: u'\ufe94\ufea4\ufed4\ufebb\u0020\ufead\ufe8e\ufef4\ufe98\ufea7\ufe8d' #utf code means page in arabic
                on_press: root.hide_kb() if root.iskb else root.show_kb()


#keyboard


    GridLayout:
        id: kb
        size_hint: (.6, .50)
        pos_hint: {'x':.2, 'y':.45}
        rows: 6


        Button:
            text: u'1'
            on_press: root.enter_number(page_val, 1)
        Button:
            text: u'2'
            on_press: root.enter_number(page_val, 2)
        Button:
            text: u'3'
            on_press: root.enter_number(page_val, 3)

        Button:
            text: u'4'
            on_press: root.enter_number(page_val, 4)
        Button:
            text: u'5'
            on_press: root.enter_number(page_val, 5)
        Button:
            text: u'6'
            on_press: root.enter_number(page_val, 6)

        Button:
            text: u'7'
            on_press: root.enter_number(page_val, 7)
        Button:
            text: u'8'
            on_press: root.enter_number(page_val, 8)
        Button:
            text: u'9'
            on_press: root.enter_number(page_val, 9)
        Button:
            text: u'<-'
            on_press: page_val.text = ''
            # on_press: page_val.text = page_val.text[:-1]
        Button:
            text: u'0'
            on_press: root.enter_number(page_val, 0)
        Button:
            id: goto_page_btn
            font_name: 'arial.ttf'
            text: u'\ufee1\ufe97'
            on_press: root.goto_page(sv, box, page_val)
        TinLabel:
            opacity: 0
        TinLabel:
            id: page_val
            size_hint: (1, .1)
            text: ''
        TinLabel:
            opacity:0



#legend image

    FloatLayout:
        id: lgd
        color: 1, 1, 1, 1
        size_hint: (1., 1.)
        pos_hint: {'x': .0, 'y': .0}
        orientation: 'vertical'
        on_touch_down: root.hide_lgd()

        Image:
            size: lgd.size
            pos: lgd.pos
            #source: 'free.png'
            color: .0, .0, .0, 1
            allow_stretch: True
        Image:
            size: lgd.size
            pos: lgd.pos
            source: 'legend.png'
            allow_stretch: True



    ''')

class TinAnimation(Animation):
    def __init__(self, **kw):
        super(TinAnimation, self).__init__()
        # Initialize
        self._clock_installed = False
        self._duration = kw.pop('d', kw.pop('duration', 1.))
        self._transition = kw.pop('t', kw.pop('transition', 'linear'))
        self._step = kw.pop('s', kw.pop('step', ANIM_STEP))
        if isinstance(self._transition, string_types):
            self._transition = getattr(AnimationTransition, self._transition)
        self._animated_properties = kw
        self._widgets = {}






class TinScrollView(ScrollView):
    spd = 10000
    def stop(self):
        TinAnimation.stop_all(self, 'scroll_x', 'scroll_y')
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
            TinAnimation.stop_all(self, 'scroll_x', 'scroll_y')
            TinAnimation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp
    def on_scroll_start(self, touch, check_children=True):
        if check_children:
            touch.push()
            touch.apply_transform_2d(self.to_local)
            if self.dispatch_children('on_scroll_start', touch):
                touch.pop()
                return True
            touch.pop()

        if not self.collide_point(*touch.pos):
            touch.ud[self._get_uid('svavoid')] = True
            return
        if self.disabled:
            return True
        if self._touch or (not (self.do_scroll_x or self.do_scroll_y)):
            return self.simulate_touch_down(touch)

        # handle mouse scrolling, only if the viewport size is bigger than the
        # scrollview size, and if the user allowed to do it
        vp = self._viewport
        if not vp:
            return True
        scroll_type = self.scroll_type
        ud = touch.ud
        scroll_bar = 'bars' in scroll_type

        # check if touch is in bar_x(horizontal) or bay_y(bertical)
        ud['in_bar_x'] = ud['in_bar_y'] = False
        width_scrollable = vp.width > self.width
        height_scrollable = vp.height > self.height
        bar_pos_x = self.bar_pos_x[0]
        bar_pos_y = self.bar_pos_y[0]

        d = {'b': True if touch.y < self.y + self.bar_width else False,
             't': True if touch.y > self.top - self.bar_width else False,
             'l': True if touch.x < self.x + self.bar_width else False,
             'r': True if touch.x > self.right - self.bar_width else False}
        if scroll_bar:
            if (width_scrollable and d[bar_pos_x]):
                ud['in_bar_x'] = True
            if (height_scrollable and d[bar_pos_y]):
                ud['in_bar_y'] = True

        if vp and 'button' in touch.profile and \
                touch.button.startswith('scroll'):
            btn = touch.button
            m = self.scroll_wheel_distance
            e = None

            if ((btn == 'scrolldown' and self.scroll_y >= 1) or
                (btn == 'scrollup' and self.scroll_y <= 0) or
                (btn == 'scrollleft' and self.scroll_x >= 1) or
                    (btn == 'scrollright' and self.scroll_x <= 0)):
                return False


            return True

        in_bar = ud['in_bar_x'] or ud['in_bar_y']
        if scroll_type == ['bars'] and not in_bar:
            return self.simulate_touch_down(touch)

        if in_bar:
            if (ud['in_bar_y'] and not
                    self._touch_in_handle(
                        self._handle_y_pos, self._handle_y_size, touch)):
                self.scroll_y = (touch.y - self.y) / self.height
            elif (ud['in_bar_x'] and not
                    self._touch_in_handle(
                        self._handle_x_pos, self._handle_x_size, touch)):
                self.scroll_x = (touch.x - self.x) / self.width

        # no mouse scrolling, so the user is going to drag the scrollview with
        # this touch.
        self._touch = touch
        uid = self._get_uid()

        #block touch scroll when auto-scrolling
        if scrolling:
            return
        
        ud[uid] = {
            'mode': 'unknown',
            'dx': 0,
            'dy': 0,
            'user_stopped': in_bar,
            'frames': Clock.frames,
            'time': touch.time_start}
        if self.do_scroll_x and self.effect_x and not ud['in_bar_x']:
            self._effect_x_start_width = self.width
            self.effect_x.start(touch.x)
            self._scroll_x_mouse = self.scroll_x
        if self.do_scroll_y and self.effect_y and not ud['in_bar_y']:
            self._effect_y_start_height = self.height
            #searched night and morning to find out
            #how to modify scroll friction, default is 0.05
            self.effect_y.friction = 0.00
            self.effect_y.start(touch.y)
            self._scroll_y_mouse = self.scroll_y

        if not in_bar:
            Clock.schedule_once(self._change_touch_mode,
                                self.scroll_timeout / 1000.)
        return True

class TinLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.5, .5, .5, 1)
            Rectangle(pos=self.pos, size=self.size)






class Tin(FloatLayout):


    ismenu = 1
    iskb = 1
    islgd = 1
    isfirsttime = 1
    isspd_up= 0
    isspd_dwn= 0
    step = 1
    mem = 0
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

        if self.isfirsttime:
            self.hide_kb()
            self.hide_lgd()
            self.isfirsttime = 0

        self.check_key_rep(bl, sv)


        self.curt_page = int(((1-sv.scroll_y)*(LAST_PAGE))+1.5)

        self.updt_pb()
        #many calculation in the next line of code : 
        #1-sv.scroll_y because scroll_y is reversed
        #LAST_PAGE-1 
        #+1.5 is for updating page number at the midle of page 
        lbl.text = str(self.curt_page)
        self.ids.menu_btn.text = str(self.tell_hizb())
        lbl_spd.text = str(sv.spd)
        lbl_siz.text = str(bl.size_hint[1])

        #he next linesare for manual page's texture buffer handler

        mid= int(((1-sv.scroll_y)*(LAST_PAGE)))

        beg= mid-1
        end= mid+2
        if beg < 0 : beg = 0
        if end > LAST_PAGE : end = LAST_PAGE



        # for i in range(0, beg+1):
        #     bl.children[LAST_PAGE- i].source = 'free.jpg'

        # for i in range(end, LAST_PAGE+1):
        #     bl.children[LAST_PAGE- i].source = 'free.jpg'

        def refresh():
            c=0
            for i in range(beg, end+1):
                c+=1
                strg= ('pages/page_' + str(i) + '.jpg')
                bl.children[LAST_PAGE- i].source = strg
                bl.children[LAST_PAGE- i].size_hint_x = 1
                self.mem = self.curt_page
                # print("in threath" + str(c))
            

        if self.mem != self.curt_page:
            refresh()
            #the second choice for asyncronous image loading
            #is using the thread as folowing:
            # threading.Thread(target = refresh()).start()

    #functions for buttons

    #@run_on_ui_thread
    def autoscroll(self, sv, box, autoscroll_btn):
        if not scrolling :
            sv.stop()
            sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
            global scrolling
            scrolling = 1
            autoscroll_btn.text = u'\ufed1\ufed7\ufeed\ufe98\ufedf\ufe8d' #stop in arabic
            # activity.mActivity.getWindow().addFlags(params.FLAG_KEEP_SCREEN_ON)

        else :
            sv.stop()
            global scrolling
            scrolling = 0
            autoscroll_btn
            autoscroll_btn.text = u'\ufe93\ufe83\ufead\ufed8\ufedf\ufe8d' #read in arabic

    def spd_dwn(self, sv, box):
            sv.spd = sv.spd - self.step
            if scrolling:
                sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
            # print sv.spd * (LAST_PAGE - self.curt_page)
            # print LAST_PAGE
            # print self.curt_page
            # print sv.spd
            #popup = Popup(title='im scrolling', size_hint=(0.5, 0.5))
            #popup.open()
        
    def spd_up(self, sv, box):
        sv.spd = sv.spd + self.step
        if scrolling:
            sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )
    
    def goto_page(self, sv, box, page_val):
        self.hide_kb()
        if page_val.text == '':
            return
        sv.scroll_to(box.children[LAST_PAGE - int(page_val.text) +1], d= 0)
        global scrolling
        scrolling = 0
    
    def check_key_rep(self, box, sv):
        if self.isspd_up and sv.spd < 400:
            self.spd_up(sv, box)

        if self.isspd_dwn and sv.spd > 20:
            self.spd_dwn(sv, box)
            self.isspd_up=0 


    def siz_up(self, box):
        box.size_hint[1]+= 20
    
    def siz_dwn(self, box):
        box.size_hint[1]-= 20


    def show_menu(self):
        if not self.ismenu:
            self.ids.menu.opacity = 1
            self.ids.menu.size_hint_x = .9
            self.ismenu = 1    
            
    def hide_menu(self):
        if self.ismenu:
            self.ids.menu.opacity = 0
            self.ids.menu.size_hint_x = .0
            self.ismenu = 0
        self.hide_kb()

    def show_kb(self):
        if not self.iskb:
            self.ids.kb.opacity = 1
            self.ids.kb.size_hint_x = .6
            self.iskb = 1

    def hide_kb(self):
        if self.iskb:
            self.ids.kb.opacity = 0
            self.ids.kb.size_hint_x = .0
            self.iskb = 0

    def show_lgd(self):
        if not self.islgd:
            self.ids.lgd.opacity = 1
            self.ids.lgd.size_hint_x = 1
            self.ids.lgd.size_hint_y = 1
            self.islgd = 1

    def hide_lgd(self):
        if self.islgd:
            self.ids.lgd.opacity = 0
            self.ids.lgd.size_hint_x = 0
            self.ids.lgd.size_hint_y = 0
            self.islgd = 0
    def reverse(self,sv,box):
        sv.stop()
        sv.scroll_y += 0.0002
        sv.scroll_to(box.children[0], d= sv.spd * (LAST_PAGE - self.curt_page) )


    # image = Image(source='legend.png')
    
    # popup = Popup(title='alwan legend',
    #                 size_hint=(0.98, 0.98),
    #                 content=image)

    # image.bind(on_touch_down=popup.dismiss)

    # popup.open()

    def enter_number(self, page_val, number):
        page_val.text += (str)(number)
        if (int)(page_val.text) > 604:
            page_val.text = u'604'
        if page_val.text == '0':
            page_val.text = u''

    def tell_hizb(self):
        x = (self.curt_page-2)/10 +1
        if x > 60:
            return 60
        if x < 1:
            return 1
        return x

    def updt_pb(self):
        if self.curt_page > 601:
            self.ids.pb.value = 100
            return
        if self.curt_page < 2:
            self.ids.pb.value = 0
            return
        x = (self.curt_page-2)/10 +1
        #first failed method
        # self.ids.pb.value = ((self.curt_page-2)%10)*10
        #second failed methode
        # self.ids.pb.value = (1 - self.ids.sv.scroll_y * 60 * 100)%100
        #correct method -for now !-
        #self.ids.pb.value = ( (1- self.ids.sv.scroll_y - (1-605.5/604)) - (float((((self.curt_page -2) /10)*10)+2)/604) )*100*60
        i = 1- self.ids.sv.scroll_y
        i *= 60
        i -= 0.05
        b = 1
        a = 2
        t = 604
        p = t - a - b
        self.ids.pb.value = ((i-(b/t))*t/p)
        i = self.ids.pb.value
        i -= x-1
        i *= 100
        if i > 100:
            i %= 100
        self.ids.pb.value = i
        print i-(b/t)
        print self.ids.pb.value

class TinApp(App):

    global Window
    global wdg


    def build(self):

        # @run_on_ui_thread
        # def android_setflag(self):
        #     PythonActivity.mActivity.getWindow().addFlags(Params.FLAG_KEEP_SCREEN_ON)

        #str(int(5000)        
        #Window.clearcolor = (.95,.95,.95,1)
        #Window.size = (700, 1400)
        Window.set_title('Quran Tin')
        self.title = 'Quran Tin'
        self.icon = 'tin.png'
        #self.presplash = Image(source= 'tin_splash.png', allow_stretch= False)
        self.wdg = Tin(size= Window.size)
        main_wdg = self.wdg

        #finaly found the way for calling object from kv file
        sv  = main_wdg.ids.sv
        box = main_wdg.ids.box


        lbl = main_wdg.ids.lbl    
        lbl_scrl_spd = main_wdg.ids.lbl_scrl_spd
        lbl_viw_siz = main_wdg.ids.lbl_viw_siz

        #restore last session7
        try:
            f = open("save.dat")
            self.curt_page = f.readline()
            box.size_hint[1] = int(f.readline())
            sv.spd = int(f.readline())
            f.close()
        except:
            self.curt_page = 0
            box.size_hint[1] = 500
            sv.spd = 80
        
        
    # initializing graphic objects
        
        #fill boxlayout with pages
        # for i in reversed(range(FIRST_PAGE, LAST_PAGE)):
        for i in range(FIRST_PAGE, LAST_PAGE+1):
            #strg =('pages/page_' + str(i) + '.jpg')
            img = AsyncImage(allow_stretch= True)
            box.add_widget(img, len(box.children))


        sv.scroll_y = 1 - float(self.curt_page)/604
        Clock.schedule_interval(main_wdg.update, 1.0 / 30.0)
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