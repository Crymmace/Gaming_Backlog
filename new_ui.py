from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from pathlib import Path
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import functions as func

Builder.load_file("design.kv")


class RootWidget(ScreenManager):
    pass


class HomeScreen(Screen):
    def view_backlog(self):
        self.manager.current = "view_backlog"


class ViewBacklogScreen(Screen):
    def get_games(self):
        return RV().build()


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': i} for i in func.get_games()]

    def build(self):
        return self


class CreateBacklogScreen(Screen):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()
