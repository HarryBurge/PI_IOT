from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from kivy.graphics.instructions import Canvas
from kivy.graphics import Rectangle
from kivy.graphics import Color
# from kivy.garden.circulardatetimepicker import CircularTimePicker, CircularNumberPicker, CircularMinutePicker

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

import datetime
import webbrowser
import copy

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class IOTApp(App):

    def build(self):

        background_image= Image(source='cool-background.jpeg', allow_stretch=True, keep_ratio=False)

        self.sm= ScreenManager(transition= SwapTransition())
        self.sm.add_widget(HibernateScreen(self.sm, name='Hibernate'))

        app= FloatLayout()
        app.add_widget(background_image)
        app.add_widget(self.sm)

        return app


class HibernateScreen(Screen):

    def __init__(self, screenmanager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screenmanager = screenmanager

        self.time = Label(text='No time', markup=True)

        unlock = Button(background_color= (0,0,0,0))
        unlock.bind(on_press=self.unlock_callback)

        Clock.schedule_interval(self.time_update, 0.5)
        self.add_widget(self.time)
        self.add_widget(unlock)

    
    def time_update(self, tom):
        current_time = datetime.datetime.now()  
        self.time.text = '[b][size=150]' + str(current_time.hour) + ':' + str(current_time.minute) + ':' + str(current_time.second) + '[/size][/b]\n[size=50]' + str(current_time.day) + ' ' + months[current_time.month] + ' - ' + str(current_time.year) + '[/size]'

    
    def unlock_callback(self, *args):
        self.screenmanager.switch_to(MainScreen(self.screenmanager))


class MainScreen(Screen):

    def __init__(self, screenmanager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screenmanager = screenmanager
        self.timer_on = False

        maingrid = GridLayout(cols=3)
        leftgrid = GridLayout(rows= 2)
        middlegrid = GridLayout(cols=2)
        rightgrid = GridLayout(rows=2)

        leftsubgrid = GridLayout(cols=2, rows=2)
        rightsubgrid = GridLayout(cols=2)

        rightsubsubgrid = GridLayout(rows=2)

        # Widgets
        self.time_widget = Label(text='No time', markup=True)
        Clock.schedule_interval(self.time_update, 1)

        def time_update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = [self.size[0] - 10, self.size[1] - 10]

        with self.time_widget.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            self.time_widget.rect = Rectangle(size=[self.time_widget.size[0] - 10, self.time_widget.size[1] - 10], pos=self.time_widget.pos)

        self.time_widget.bind(pos=time_update_rect, size=time_update_rect)

        hibernate = Tile(image_normal = 'lock_up.png', background_color=[0,0,0,0])
        hibernate.bind(on_press=self.hibernate_callback)

        youtube = Tile(image_normal = 'youtube_up.png', background_color=[0,0,0,0])
        youtube.bind(on_press= self.youtube_callback)

        spotify = Tile(image_normal= 'Spotify_up.png', background_color=[0,0,0,0])
        spotify.bind(on_press= self.spotify_callback)

        volume = Slider(orientation='vertical', min=0, max=100, value=25, cursor_image='slider.png', cursor_height=40, cursor_width=100, background_width=100)
        #pip install pyalsaaudio then do import alsaaudio
        # m = alsaaudio.Mixer()
        # current_volume = m.getvolume() # Get the current Volume
        # m.setvolume(70) # Set the volume to 70%.
        # m = alsaaudio.Mixer('PCM')
        def vol_update_rect(self, *args):
            volume.rect.pos = volume.pos
            volume.rect.size = [volume.size[0] - 10, volume.size[1] - 10]

        with volume.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            volume.rect = Rectangle(size=[volume.size[0] - 10, volume.size[1] - 10], pos=volume.pos)

        volume.bind(pos=vol_update_rect, size=vol_update_rect)


        self.timerbutton = Button(text='Timer', background_color=[0,0,0,0], font_size=50, bold=True)
        self.timerbutton.bind(on_press= self.timer_callback)

        def timer_update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = [self.size[0] - 10, self.size[1] - 10]

        with self.timerbutton.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            self.timerbutton.rect = Rectangle(size=[self.timerbutton.size[0] - 10, self.timerbutton.size[1] - 10], pos=self.timerbutton.pos)

        self.timerbutton.bind(pos=timer_update_rect, size=timer_update_rect)

        foodchooser = Tile(image_normal = 'food_chooser.png', background_color=[0,0,0,0])
        foodchooser.bind(on_press= self.foodchooser_callback)

        # Add widgets
        # Left Grid
        leftgrid.add_widget(self.timerbutton)

        leftsubgrid.add_widget(spotify)
        leftsubgrid.add_widget(youtube)
        leftsubgrid.add_widget(Label())
        leftsubgrid.add_widget(Label())

        # Middle Grid
        middlegrid.add_widget(foodchooser)
        for i in range(7):
            middlegrid.add_widget(Label())

        # Right Grid
        rightgrid.add_widget(self.time_widget)

        rightsubgrid.add_widget(volume)

        rightsubsubgrid.add_widget(Label())
        rightsubsubgrid.add_widget(hibernate)

        # Do columns
        leftgrid.add_widget(leftsubgrid)
        rightsubgrid.add_widget(rightsubsubgrid)
        rightgrid.add_widget(rightsubgrid)

        maingrid.add_widget(leftgrid)
        maingrid.add_widget(middlegrid)
        maingrid.add_widget(rightgrid)

        self.add_widget(maingrid)


    def time_update(self, tom):
        current_time = datetime.datetime.now()  
        self.time_widget.text = '[b][size=70]' + str(current_time.hour) + ':' + str(current_time.minute) + ':' + str(current_time.second) + '[/size][/b]\n[size=20]' + str(current_time.day) + ' ' + months[current_time.month] + ' - ' + str(current_time.year) + '[/size]'
        if self.timer_on:
            if self.timerbutton.text != 'Finished':
                secs = int(self.timerbutton.text.split(':')[0])*60 + int(self.timerbutton.text.split(':')[1])
                secs -= 1
                self.timerbutton.text = str(secs//60) + ':' + str(secs%60)

    def hibernate_callback(self, *args):
        self.screenmanager.switch_to(HibernateScreen(self.screenmanager))
    def youtube_callback(self, *args):
        webbrowser.open('https://www.youtube.com/')
    def spotify_callback(self, *args):
        webbrowser.open('https://open.spotify.com/')
    def alarm_callback(self, *args):
        self.timerbutton.text = 'Finished'
        self.timerbutton.background_color = (0, 50, 0, 1)
    def foodchooser_callback(self, *args):
        self.screenmanager.switch_to(FoodChooser(self.screenmanager))
    def timer_callback(self, *args):

        if not self.timer_on:

            grid = GridLayout(cols=1)
            b_grid = GridLayout(rows=1, size_hint=(1, 0.2))

            close = Button(text='Close me!')
            set_timer = Button(text='Set Timer!')

            minspicker = GridLayout(cols=1)

            self.mins = Label(text='0', size_hint=(1,0.2), font_size=50, bold=True)

            self.numpad = GridLayout(cols=3, rows=4, spacing=[20,20], padding=[20,20,20,20])

            def numberpush(self, button):
                if self.mins.text == '0':
                    self.mins.text = str(button.text)
                else:
                    self.mins.text = self.mins.text + str(button.text)

            for i in range(7, 10):
                temp = Button(text=str(i))
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)
            for i in range(4, 7):
                temp = Button(text=str(i))
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)
            for i in range(1,4):
                temp = Button(text=str(i))
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)

            self.numpad.add_widget(Label())

            temp = Button(text=str('0'))
            temp.bind(on_press= lambda i: numberpush(self, i))
            self.numpad.add_widget(temp)

            def numberremove(self):
                if len(self.mins.text) <= 1:
                    self.mins.text = '0'
                else:
                    self.mins.text = self.mins.text[:-1]

            temp = Button(text='BackSpace')
            temp.bind(on_press= lambda i: numberremove(self))
            self.numpad.add_widget(temp)

            minspicker.add_widget(self.mins)
            minspicker.add_widget(self.numpad)

            grid.add_widget(minspicker)
            b_grid.add_widget(close)
            b_grid.add_widget(set_timer)

            grid.add_widget(b_grid)

            self.popup = Popup(title='Mins Timer', content=grid, auto_dismiss=False)

            def close_popup(*args):
                self.popup.dismiss()
                self.timer_on = False

            close.bind(on_press=close_popup)

            def set_timer_b(*args):
                self.timer_on = True
                self.timerclock = Clock.schedule_once(self.alarm_callback, int(self.mins.text)*60)
                self.timerbutton.text = self.mins.text + ':0'
                self.popup.dismiss()

            set_timer.bind(on_press=set_timer_b)

            self.popup.open()

        elif self.timerbutton.text== 'Finished':
            self.timerbutton.text = 'Timer'
            self.timerbutton.background_color = (0,0,0,0)
            self.timer_on = False

        else:
            self.timerbutton.text = 'Finished'
            self.timerbutton.background_color = (1, 0, 0, 1)
            self.timerclock.cancel()


class FoodChooser(Screen):

    def __init__(self, screenmanager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screenmanager = screenmanager

        ui_grid = GridLayout(rows=1)

        main_grid = GridLayout(rows=2, cols=1)
        buttons_grid = GridLayout(cols=1, size_hint=(0.2, 1))

        # viewer
        self.txtviewer = ScrollView()

        def txtviewer_update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = [self.size[0] - 10, self.size[1] - 10]

        with self.txtviewer.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            self.txtviewer.rect = Rectangle(size=[self.txtviewer.size[0] - 10, self.txtviewer.size[1] - 10], pos=self.txtviewer.pos)

        self.txtviewer.bind(pos=txtviewer_update_rect, size=txtviewer_update_rect)
        # ---

        # listings in viewer
        self.scoll_view_update_callback()
        # ---

        # title
        temp = Label(text='All Food Ideas', size_hint=(1, 0.1), font_size=50, bold=True)

        def title_update_rect(self, *args):
            temp.rect.pos = temp.pos
            temp.rect.size = [temp.size[0] - 10, temp.size[1] - 10]

        with temp.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            temp.rect = Rectangle(size=[temp.size[0] - 10, temp.size[1] - 10], pos=temp.pos)

        temp.bind(pos=title_update_rect, size=title_update_rect)
        # ---

        main_grid.add_widget(temp)
        main_grid.add_widget(self.txtviewer)

        # Buttons
        add_new = Tile(image_normal= 'plus_sign.png', background_color=(0,0,0,0))
        add_new.bind(on_press= self.addnew_callback)
        # ---

        buttons_grid.add_widget(Button())
        buttons_grid.add_widget(add_new)

        ui_grid.add_widget(main_grid)
        ui_grid.add_widget(buttons_grid)

        self.add_widget(ui_grid)

    def scoll_view_update_callback(self, *args):
        self.txtviewer.clear_widgets()

        temp = open('food_list.txt', 'r')
        lines = temp.read().split('\n')
        temp.close()

        lists = GridLayout(cols=1)

        for i in lines:
            temp_b = Label(text= str(i))
            lists.add_widget(temp_b)

        self.txtviewer.add_widget(lists)
    def addnew_callback(self, *args):
        temp = open('food_list.txt', 'a')
        temp.write('\n' + input('>>')) # Create a popup
        temp.close()
        self.scoll_view_update_callback()
        

class Tile(Button):

    def __init__(self, image_normal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with self.canvas.before:
            Color(0.73828125, 0.48828125, 0.2890625, 0.5)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.img = Image(source=image_normal)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = [self.size[0] - 10, self.size[1] - 10]
        self.img.pos = self.pos
        self.img.size = [self.size[0] - 10, self.size[1] - 10]


if __name__ == '__main__':
    Window.maximize()
    IOTApp().run()