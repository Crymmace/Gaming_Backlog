from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from howlongtobeatpy import HowLongToBeat
from backend import Database
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable


Builder.load_file("design.kv")
database = Database("backlog.db")


class Game:
    def __init__(self, name, genre):
        self.name = name
        self.genre = genre

    def __repr__(self):
        return "{}, {}".format(self.name, self.genre)


def get_games():
    all_games = []
    data = database.view()
    for row in data:
        temp_game = Game(row.game, row.genre)
        all_games.append(temp_game)
    return all_games


def find_game(game_name):
    results = HowLongToBeat(0.0).search(game_name, similarity_case_sensitive=False)
    return results


def submit():
    data = (game, genre)
    database.insert(data, data)


def remove():

    if database.search(data, data) > 0:
        data = database.search(data, data).first()
        database.delete(data)


class HomeScreen(Screen):
    def create_backlog(self):
        self.manager.current = "create_backlog"

    def view_backlog(self):
        self.manager.current = "view_backlog"


class CreateBacklogScreen(Screen):
    def show_game_results(self, game_name):
        games = find_game(game_name)
        if games:
            table = Table()
            table.populate(games)
            table.build()
            table.run()


class Table(MDApp):
    data_tables = None
    game_list = []

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            column_data=[
                ("No.", dp(30)),
                ("Game", dp(30)),
                ("Link", dp(30)),
            ],
            row_data=self.game_list,
        )
        layout.add_widget(self.data_tables)
        return layout

    def populate(self, games):
        x = 1
        for game in games:
            self.game_list.append((str(x), game.game_name, game.game_web_link))
            x += 1


class ViewBacklogScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()

# TODO: Implement API, make pretty, bug fixes, improve functionality, implement exporting
# TODO: Convert from flask to Kivy.
# TODO: Switch from postgres to SQL lite.
# TODO: Make links clickable, add ability to select data from rows, add ability to add selection to database.
