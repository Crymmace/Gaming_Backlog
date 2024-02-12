import functions
import PySimpleGUI as gui

new_games = []
web = []
images = []
main_story = []
extras = []
completionist = []
entries = []


genres = []
for entry in functions.grab_genres():
    genres.append(entry)

selected_genre = []
for entry in functions.search_preference_genre():
    if entry:
        selected_genre.append(entry[0].split(","))
        selected_genre = selected_genre[0]

options = ["Main Story", "Main Story and Extras", "Completionist"]
selected_option = ""
if functions.search_preference_completion():
    selected_option = functions.search_preference_completion()
    selected_option = selected_option[0][0]

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
    [gui.Listbox(values=options, key="choice", enable_events=True, size=(20, 5))],
    [gui.Text(f"Current selection is: {selected_option}", key="text")],
    [gui.Listbox(values=genres, key="genre_options", enable_events=True, size=(20, 5)), gui.Button("-->"),
     gui.Button("<--"), gui.Listbox(values=selected_genre, key="genre_choice", enable_events=True, size=(20, 5))],
    [gui.Button("Save Preferences")]
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

        case "-->":
            genre_choice = values['genre_options'][0]
            selected_genre.append(genre_choice)
            genres.remove(genre_choice)
            window['genre_options'].update(values=genres)
            window['genre_choice'].update(values=selected_genre)

        case "<--":
            genre_choice = values['genre_choice'][0]
            genres.append(genre_choice)
            genres = sorted(genres)
            selected_genre.remove(genre_choice)
            window['genre_options'].update(values=genres)
            window['genre_choice'].update(values=selected_genre)

        case "Save Preferences":
            completion = values['choice'][0]
            genre = selected_genre
            new_genre = []
            for entry in genre:
                new_genre.append(entry.replace("\n", ""))
            print(new_genre)
            new_genre = ' ,'.join(new_genre)
            print(new_genre)
            print(completion)
            if not functions.get_preference():
                functions.add_preference(completion, new_genre)
            if functions.get_preference():
                functions.update_preference(1, completion, new_genre)

            window['genre_choice'].update(values=selected_genre)
            window['text'].update(values=f"Current selection is: {selected_option}")

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

                print(genre)

                rating = functions.get_metacritic_score(game_selection)
                fun = functions.calculate_fun_quotient(rating, main_selection, extra_selection,
                                                       completionist_selection, selected_option)

                for entry in selected_genre:
                    if entry[:-1] in genre:
                        entries.append(entry)

                fun = fun + len(entries)
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
                game_to_delete = game_to_delete.split(" ")
                games = functions.get_games()
                functions.remove_from_database(game_to_delete[0])
                functions.get_games()
                window['game'].update(value="")
            except IndexError:
                gui.popup("Please select an item.", font=("Helvetica", 20))

        case "Exit":
            break

        case gui.WIN_CLOSED:
            break

window.close()

# TODO: Clean up UI
# TODO: Figure out why UI is slow
