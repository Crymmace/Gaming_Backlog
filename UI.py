from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from howlongtobeatpy import HowLongToBeat
from database import Database
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
import webbrowser


Builder.load_file("design.kv")
database = Database("backlog.db")


class Game:
    def __init__(self, game):
        self.game = game

    def __repr__(self):
        return "{}".format(self.game)


def get_games():
    all_games = []
    data = database.view()
    for row in data:
        temp_game = Game(row.game)
        all_games.append(temp_game)
    return all_games


def find_game(game):
    results = HowLongToBeat(0.0).search(game, similarity_case_sensitive=False)
    return results


def submit(game):
    database.insert(game)


def remove(game):
    if database.search(game) > 0:
        data = database.search(game).first()
        database.delete(data)


class HomeScreen(Screen):
    def create_backlog(self):
        self.manager.current = "create_backlog"

    def view_backlog(self):
        self.manager.current = "view_backlog"


class CreateBacklogScreen(Screen):
    @staticmethod
    def show_game_results(game_name):
        games = find_game(game_name)
        if games:
            table = Table()
            table.populate(games)
            table.build()
            table.run()


class Table(MDApp):
    data_tables = None
    game_list = []
    old_checks = []

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            size_hint=(1.0, 0.6),
            check=True,
            column_data=[
                ("No.", dp(30)),
                ("Game", dp(30)),
                ("Link", dp(90)),
            ],
            row_data=self.game_list,
        )

        self.data_tables.bind(on_row_press=self.on_row_press)
        layout.add_widget(self.data_tables)
        return layout

    def populate(self, games):
        x = 1
        for game in games:
            self.game_list.append((str(x), game.game_name, game.game_web_link))
            x += 1

    def on_row_press(self, instance_table, instance_row):
        start_index, end_index = instance_row.table.recycle_data[instance_row.index]["range"]
        checks = self.data_tables.get_row_checks()
        link = instance_row.table.recycle_data[end_index]["text"]
        is_present = False
        for check in checks:
            if check[-1] == link:
                is_present = True
        for check in self.old_checks:
            if check[-1] == link:
                is_present = True
        self.old_checks = checks
        if not is_present:
            webbrowser.open(link)


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
# TODO: Add ability to select data from rows, add ability to add selection to database
# TODO: Fix checkbox affecting on row click functionality
# TODO: Implement selection wizard with metacritic API
# TODO: Implement metacritic API
