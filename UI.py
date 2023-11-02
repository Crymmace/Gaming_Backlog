import functions
import PySimpleGUI as gui
import time

new_games = []
web = []
time_to_beat = []

gui.theme("Black")

label = gui.Text("Type in a game")
input_box = gui.InputText(tooltip="Enter game", key="game")
search_button = gui.Button("Search")
add_button = gui.Button("Add")
list_box = gui.Listbox(values=new_games, key="games",
                       enable_events=True, size=(45, 10))
view_button = gui.Button("View")
delete_button = gui.Button("Delete")
exit_button = gui.Button("Exit")

window = gui.Window("My To-Do App",
                    layout=[[label],
                            [input_box, search_button, add_button],
                            [list_box, view_button, delete_button],
                            [exit_button]],
                    font=('Helvetica', 20))


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
            for times in new_game:
                time_to_beat.append(times.main_story)
            window['games'].update(values=new_games)

        case "Add":
            selected_game = values['games'][0]
            print(selected_game)
            selection = new_games.index(selected_game)
            print(selection)

            game_selection = functions.game_selection(new_games, selection)
            url_selection = functions.url_selection(web, selection)
            time_selection = functions.time_selection(time_to_beat, selection)
            genre = functions.get_genre(url_selection)
            if not genre:
                genre = functions.get_genre2(url_selection)
            rating = functions.get_metacritic_score(game_selection)
            fun = functions.calculate_fun_quotient(rating, time_selection)
            functions.add_to_database(game_selection, genre, rating, fun, time_selection)

            games = functions.get_games()
            new_game = values['games']
            window['games'].update(values=games)

            time.sleep(0.5)
            games = functions.get_games()
            new_games.clear()

        case "View":
            games = functions.get_games()
            new_game = values['games']
            print(new_game)
            print(functions.find_game(new_game))
            window['games'].update(values=games)
            time.sleep(0.5)
            games = functions.get_games()

        case "Delete":
            try:
                game_to_delete = values['games'][0]
                games = functions.get_games()
                functions.remove_from_database(game_to_delete[0])
                functions.get_games()
                window['games'].update(values=games)
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
