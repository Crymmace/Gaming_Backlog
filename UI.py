import functions
import PySimpleGUI as gui

new_games = []
web = []
images = []
main_story = []
extras = []
completionist = []
genres = []
selected_genres = []
options = ["1. Main Story", "2. Main Story and Extras", "3. Completionist"]

gui.theme("BlueMono")

search_layout = [
    [gui.Text("Type in a game")],
    [gui.InputText(tooltip="Enter game", key="game")],
    [gui.Button("Search")],
    [gui.Listbox(values=new_games, key="games", enable_events=True, size=(45, 10))],
    [gui.Button("Add")]
]

database_layout = [
    [gui.Listbox(values=new_games, key="database_games", enable_events=True, size=(45, 10)), gui.Button("Delete")],
    [gui.Button("Update")],
    [gui.Button("Exit")],
]

preference_layout = [
    [gui.Listbox(values=options, key="choice", enable_events=True, size=(20, 5)), gui.Button("Select")],
    [gui.Text("", key="text")]
]

tab_group = [
    [gui.TabGroup(
        [[gui.Tab("Find Games", search_layout),
          gui.Tab("View Games", database_layout),
          gui.Tab("Preferences", preference_layout)]],
        tab_location='topleft')
    ]
]
window = gui.Window("My To-Do App", tab_group)

while True:
    event, values = window.read(timeout=10)
    match event:
        case "Search":
            id_ = values["game"]
            new_game = functions.find_game(id_)
            for game in new_game:
                new_games.append(game.game_name)
            for url in new_game:
                web.append(url.game_web_link)
            for image in new_game:
                images.append(image.game_image_url)
            for times in new_game:
                main_story.append(times.main_story)
                extras.append(times.main_extra)
                completionist.append(times.completionist)
            window['games'].update(values=new_games)

        case "Select":
            preference = values['choice'][0][0]
            window['text'].update(value=f"{values['choice'][0]}")

        case "Add":
            try:
                selected_game = values['games'][0]

                selection = new_games.index(selected_game)

                game_selection = functions.game_selection(new_games, selection)

                url_selection = functions.url_selection(web, selection)
                main_selection = functions.time_selection(main_story, selection)
                extra_selection = functions.time_selection(extras, selection)
                completionist_selection = functions.time_selection(completionist, selection)

                genre = functions.get_genre(url_selection)

                if not genre:
                    genre = functions.get_genre2(url_selection)

                rating = functions.get_metacritic_score(game_selection)
                fun = functions.calculate_fun_quotient(rating, main_selection, extra_selection,
                                                       completionist_selection, preference)
                functions.add_to_database(game_selection, genre, rating, main_selection, extra_selection,
                                          completionist_selection, fun)

                games = functions.get_games()
                new_game = values['games']
                new_games.clear()
            except NameError:
                error = gui.popup_ok("Please select a preference.")

        case "Update":
            games = functions.get_games()
            new_game = values['games']
            window['database_games'].update(values=games)
            games = functions.get_games()

        case "Delete":
            try:
                game_to_delete = values['database_games'][0]
                games = functions.get_games()
                functions.remove_from_database(game_to_delete[0])
                functions.get_games()
                window['database_games'].update(values=games)
                window['game'].update(value="")
            except IndexError:
                gui.popup("Please select an item.", font=("Helvetica", 20))

        case "Exit":
            break

        case "todos":
            window['todo'].update(value=values['todos'][0])

        case gui.WIN_CLOSED:
            break

window.close()


