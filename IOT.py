from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.garden.circulardatetimepicker import CircularTimePicker, CircularNumberPicker, CircularMinutePicker

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window

import datetime
import webbrowser

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
        middlegrid = GridLayout(rows=1)
        rightgrid = GridLayout(rows=2)

        leftsubgrid = GridLayout(cols=2, rows=2)
        rightsubgrid = GridLayout(cols=2)

        rightsubsubgrid = GridLayout(rows=2)

        # Widgets
        self.time_widget = Label(text='No time', markup=True)
        Clock.schedule_interval(self.time_update, 0.5)

        hibernate = Button(background_normal = 'lock_up.png', background_down ='lock_down.png')
        hibernate.bind(on_press=self.hibernate_callback)

        youtube = Button(background_normal= 'youtube_up.png', background_down= 'youtube_down.png')
        youtube.bind(on_press= self.youtube_callback)

        spotify = Button(background_normal= 'Spotify_up.png', background_down= 'Spotify_down.png')
        spotify.bind(on_press= self.spotify_callback)

        volume = Slider(orientation='vertical', min=0, max=100, value=25, cursor_image='slider.png', cursor_height=40, cursor_width=100, background_width=100)
        #pip install pyalsaaudio then do import alsaaudio
        # m = alsaaudio.Mixer()
        # current_volume = m.getvolume() # Get the current Volume
        # m.setvolume(70) # Set the volume to 70%.
        # m = alsaaudio.Mixer('PCM')

        timerbutton = Button(text='Timer', background_color=[0,0,0,0])
        timerbutton.bind(on_press= self.timer_callback)

        # Add widgets
        # Left Grid
        leftgrid.add_widget(timerbutton)

        leftsubgrid.add_widget(spotify)
        leftsubgrid.add_widget(youtube)
        leftsubgrid.add_widget(Label())
        leftsubgrid.add_widget(Label())

        # Middle Grid
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
        self.time_widget.text = '[b][size=60]' + str(current_time.hour) + ':' + str(current_time.minute) + ':' + str(current_time.second) + '[/size][/b]\n[size=20]' + str(current_time.day) + ' ' + months[current_time.month] + ' - ' + str(current_time.year) + '[/size]'


    def hibernate_callback(self, *args):
        self.screenmanager.switch_to(HibernateScreen(self.screenmanager))
    def youtube_callback(self, *args):
        webbrowser.open('https://www.youtube.com/')
    def spotify_callback(self, *args):
        webbrowser.open('https://open.spotify.com/')
    def timer_callback(self, *args):

        if not self.timer_on:

            grid = GridLayout(cols=1)
            b_grid = GridLayout(rows=1, size_hint=(1, 0.2))

            close = Button(text='Close me!')
            set_timer = Button(text='Set Timer!')
            self.mins = CircularMinutePicker()

            grid.add_widget(self.mins)
            b_grid.add_widget(close)
            b_grid.add_widget(set_timer)

            grid.add_widget(b_grid)

            self.popup = Popup(content=grid, auto_dismiss=False)

            def close_popup(*args):
                self.popup.dismiss()
                self.timer_on = False

            close.bind(on_press=close_popup)

            def set_timer_b(*args):
                self.popup.dismiss()
                self.timer_on = True

            set_timer.bind(on_press=set_timer_b)

            self.popup.open()


if __name__ == '__main__':
    Window.maximize()
    IOTApp().run()