import functions
import PySimpleGUI as gui
import time

new_games = []
web = []
main_story = []
extras = []
completionist = []
genres = []
selected_genres = []
options = ["1. Main Story", "2. Main Story and Extras", "3. Completionist"]

gui.theme("Black")

label = gui.Text("Type in a game")
input_box = gui.InputText(tooltip="Enter game", key="game")
search_button = gui.Button("Search")
add_button = gui.Button("Add")
select_button = gui.Button("Select")
list_box = gui.Listbox(values=new_games, key="games",
                       enable_events=True, size=(45, 10))
choice_box = gui.Listbox(values=options, key="choice",
                         enable_events=True, size=(20, 5))
view_button = gui.Button("View")
delete_button = gui.Button("Delete")
exit_button = gui.Button("Exit")

window = gui.Window("My To-Do App",
                    layout=[[label],
                            [input_box, search_button, add_button],
                            [list_box, choice_box, select_button],
                            [view_button, delete_button, exit_button ]],
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
                main_story.append(times.main_story)
                extras.append(times.main_extra)
                completionist.append(times.completionist)
            window['games'].update(values=new_games)

        case "Select":
            preference = values['choice'][0][0]

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
                window['games'].update(values=games)

                time.sleep(0.5)
                games = functions.get_games()
                new_games.clear()
            except NameError:
                error = gui.popup_ok("Please select a preference.")

        case "View":
            games = functions.get_games()
            new_game = values['games']
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
