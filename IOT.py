from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock

import datetime

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

        self.time = Label(text='No time', size_hint= (1,1), markup=True)

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

        grid = GridLayout(cols= 6, rows= 5, spacing= (20,20))

        for i in range(6):
            for j in range(5):
                grid.add_widget(Button())

        self.add_widget(grid)


if __name__ == '__main__':
    IOTApp().run()