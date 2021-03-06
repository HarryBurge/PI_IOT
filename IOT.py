from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.vkeyboard import VKeyboard
from kivy.uix.textinput import TextInput

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
from random import randint
from allrecipes import AllRecipes

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

        recipe = Tile(image_normal= 'recipe.png', background_color=[0,0,0,0])
        recipe.bind(on_press= self.recipe_callback)

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
        leftsubgrid.add_widget(recipe)
        leftsubgrid.add_widget(foodchooser)

        # Middle Grid
        for i in range(8):
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
    def recipe_callback(self, *args):
        self.screenmanager.switch_to(RecipeFinder(self.screenmanager))
    def timer_callback(self, *args):

        if not self.timer_on:

            grid = GridLayout(cols=1)
            b_grid = GridLayout(rows=1, size_hint=(1, 0.2))

            close = Button(text='Close me!', font_size=50, bold=True)
            set_timer = Button(text='Set Timer!', font_size=50, bold=True)

            minspicker = GridLayout(cols=1)

            self.mins = Label(text='0', size_hint=(1,0.2), font_size=50, bold=True)

            self.numpad = GridLayout(cols=3, rows=4, spacing=[20,20], padding=[20,20,20,20])

            def numberpush(self, button):
                if self.mins.text == '0':
                    self.mins.text = str(button.text)
                else:
                    self.mins.text = self.mins.text + str(button.text)

            for i in range(7, 10):
                temp = Button(text=str(i), font_size=50, bold=True)
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)
            for i in range(4, 7):
                temp = Button(text=str(i), font_size=50, bold=True)
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)
            for i in range(1,4):
                temp = Button(text=str(i), font_size=50, bold=True)
                temp.bind(on_press= lambda i: numberpush(self, i))
                self.numpad.add_widget(temp)

            self.numpad.add_widget(Label())

            temp = Button(text=str('0'), font_size=50, bold=True)
            temp.bind(on_press= lambda i: numberpush(self, i))
            self.numpad.add_widget(temp)

            def numberremove(self):
                if len(self.mins.text) <= 1:
                    self.mins.text = '0'
                else:
                    self.mins.text = self.mins.text[:-1]

            temp = Button(text='BackSpace', font_size=50, bold=True)
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

        random7 = Tile(image_normal='dice.png', background_color=(0,0,0,0))
        random7.bind(on_press= self.randomiser)

        back = Tile(image_normal='back.png', background_color=(0,0,0,0))
        back.bind(on_press=self.back_callback)
        # ---

        buttons_grid.add_widget(random7)
        buttons_grid.add_widget(add_new)
        buttons_grid.add_widget(back)

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
            temp_b = Label(text= str(i), font_size=30, bold=True)
            lists.add_widget(temp_b)

        self.txtviewer.add_widget(lists)
    def addnew_callback(self, *args):
        # Popup
        gird = GridLayout(cols=1)

        self.chars = Label(text='', size_hint=(1, 0.1), font_size=50, bold=True)
        gird.add_widget(self.chars)

        # Keyboard
        def keyboardpress(button):
            self.chars.text = self.chars.text + str(button.text)
        def keyboardspace(*args):
            self.chars.text = self.chars.text + ' '
        def backspace(*args):
            if len(self.chars.text) > 0:
                self.chars.text= self.chars.text[:-1]

        keyboard = GridLayout(rows=3, cols=10)

        keys_in_order = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','','z','x','c','v','b','n','m','','','']

        for key in keys_in_order:
            if key=='':
                keyboard.add_widget(Label())
            else:
                temp = Button(text=key, font_size=50, bold=True)
                temp.bind(on_press=lambda i: keyboardpress(i))
                keyboard.add_widget(temp)

        gird.add_widget(keyboard)
        # ---

        buttons = GridLayout(rows=1, size_hint=(1, 0.2))

        temp = Button(text='Space', font_size=40, bold=True)
        temp.bind(on_press=lambda i: keyboardspace(i))
        buttons.add_widget(temp)

        temp = Button(text='BackSpace', size_hint=(0.25, 1), font_size=40, bold=True)
        temp.bind(on_press=lambda i: backspace(i))
        buttons.add_widget(temp)

        quiter = Button(text='Quit', size_hint=(0.25, 1), font_size=40, bold=True)
        buttons.add_widget(quiter)

        saver = Button(text='Save', size_hint=(0.1, 1), font_size=40, bold=True)
        buttons.add_widget(saver)

        gird.add_widget(buttons)
        

        self.popup = Popup(title='New Food Item', content=gird, auto_dismiss=False)

        self.popup.open()


        def close_popup(*args):
            self.popup.dismiss()

        quiter.bind(on_press=close_popup)

        def save_item(*args):
            file = open('food_list.txt', 'a')
            file.write('\n' + self.chars.text)
            file.close()
            self.scoll_view_update_callback()
            self.popup.dismiss()

        saver.bind(on_press=save_item)
    def randomiser(self, *args):
        file = open('food_list.txt', 'r')
        lines = file.read().split('\n')

        lister = GridLayout(cols=1)

        for i in range(7):
            slec = lines[randint(0, len(lines)-1)]
            lister.add_widget(Label(text=slec, font_size=50, bold=True))

        quiter = Button(text='Quit', font_size=50, bold=True)
        lister.add_widget(quiter)

        self.popup = Popup(title='7 Food Items', content=lister, auto_dismiss=False)

        self.popup.open()

        def close_popup(*args):
            self.popup.dismiss()

        quiter.bind(on_press=close_popup)    
    def back_callback(self, *args):
        self.screenmanager.switch_to(MainScreen(self.screenmanager))


class RecipeFinder(Screen):
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
        self.scoll_view_update_callback([])
        # ---

        main_grid.add_widget(self.txtviewer)

        # Buttons
        search = Tile(image_normal= 'search.png', background_color=(0,0,0,0))
        search.bind(on_press= self.search_callback)

        back = Tile(image_normal='back.png', background_color=(0,0,0,0))
        back.bind(on_press=self.back_callback)
        # ---

        buttons_grid.add_widget(search)
        buttons_grid.add_widget(back)

        ui_grid.add_widget(main_grid)
        ui_grid.add_widget(buttons_grid)

        self.add_widget(ui_grid)

    def scoll_view_update_callback(self, items, *args):
        self.txtviewer.clear_widgets()

        lists = GridLayout(cols=1)

        def open_url(url):
            webbrowser.open(url)

        for i in items:
            menu_item = GridLayout(cols=1)

            temp_b = Button(text= str(i['name']), font_size=30, bold=True, background_color= [0,0,0,0])
            temp_b.url = i['url']
            temp_b.bind(on_press=lambda x: open_url(x.url))
            menu_item.add_widget(temp_b)

            temp_d = Button(text= str(i['description']), font_size=15, background_color= [0,0,0,0])
            temp_d.url = i['url']
            temp_d.bind(on_press=lambda x: open_url(x.url))
            menu_item.add_widget(temp_d)

            lists.add_widget(menu_item)

        self.txtviewer.add_widget(lists)

    def search_callback(self, *args):
        # Popup
        gird = GridLayout(cols=1)

        self.chars = Label(text='', size_hint=(1, 0.1), font_size=50, bold=True)
        gird.add_widget(self.chars)

        # Keyboard
        def keyboardpress(button):
            self.chars.text = self.chars.text + str(button.text)
        def keyboardspace(*args):
            self.chars.text = self.chars.text + ' '
        def backspace(*args):
            if len(self.chars.text) > 0:
                self.chars.text= self.chars.text[:-1]

        keyboard = GridLayout(rows=3, cols=10)

        keys_in_order = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','','z','x','c','v','b','n','m','','','']

        for key in keys_in_order:
            if key=='':
                keyboard.add_widget(Label())
            else:
                temp = Button(text=key, font_size=50, bold=True)
                temp.bind(on_press=lambda i: keyboardpress(i))
                keyboard.add_widget(temp)

        gird.add_widget(keyboard)
        # ---

        buttons = GridLayout(rows=1, size_hint=(1, 0.2))

        temp = Button(text='Space', font_size=40, bold=True)
        temp.bind(on_press=lambda i: keyboardspace(i))
        buttons.add_widget(temp)

        temp = Button(text='BackSpace', size_hint=(0.25, 1), font_size=40, bold=True)
        temp.bind(on_press=lambda i: backspace(i))
        buttons.add_widget(temp)

        quiter = Button(text='Quit', size_hint=(0.25, 1), font_size=40, bold=True)
        buttons.add_widget(quiter)

        search = Button(text='Search', size_hint=(0.1, 1), font_size=40, bold=True)
        buttons.add_widget(search)

        gird.add_widget(buttons)

        self.popup = Popup(title='New Food Item', content=gird, auto_dismiss=False)

        self.popup.open()

        def close_popup(*args):
            self.popup.dismiss()

        quiter.bind(on_press=close_popup)

        def search_item(*args):
            query_options = {
                "wt": self.chars.text,         # Query keywords
                "sort": "p"                # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }
            query_results = AllRecipes.search(query_options)
            self.scoll_view_update_callback(query_results)
            self.popup.dismiss()

        search.bind(on_press=search_item)

    def back_callback(self, *args):
        self.screenmanager.switch_to(MainScreen(self.screenmanager))


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
    # Window.maximize()
    IOTApp().run()