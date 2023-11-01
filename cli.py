import functions

while True:
    option = input("What would you like to do? ").lower()
    match option:
        case "add":
            game_title = input("Enter game: ")

            result = functions.find_game(game_title)
            games = []
            web = []
            time = []

            # Grabs game titles and appends to games list.
            for title in result:
                games.append(title.game_name)
            # Grabs game url and appends to web list.
            for url in result:
                web.append(url.game_web_link)
            # Grabs time it takes to beat main story and appends to time list.
            for times in result:
                time.append(times.main_story)

            # Prints out an enumerated games list.
            i = 1
            for item in games:
                print(f"{i}. {item}")
                i += 1

            # Calls select_game function with the games, web, and time lists as parameters.
            choice = int(input("Which game would you like? "))
            choice = choice - 1

            # Calls each function for game, web, and time, and assigns them to the corresponding variable.
            game_selection = functions.game_selection(games, choice)
            url_selection = functions.url_selection(web, choice)
            time_selection = functions.time_selection(time, choice)

            # Calls get_genre functions with url_selection as the parameter and assigns value to genre variable.
            genre = functions.get_genre(url_selection)
            if not genre:
                genre = functions.get_genre2(url_selection)

            # Calls get_metacritic_score functions with game_selection as the parameter
            # and assigns value to rating variable.
            rating = functions.get_metacritic_score(game_selection)

            # Calls calculate_fun_quotient function with rating and time_selection() as parameters
            # and assigns value to fun variable.
            fun = functions.calculate_fun_quotient(rating, time_selection)

            # Adds all game information to database.
            functions.add_to_database(game_selection, genre, rating, fun, time_selection)
        case "view":
            # Calls function to print entries currently in database.
            functions.get_games()
        case "delete":
            functions.get_games()
            choice = int(input("Which would you like to delete? "))
            functions.remove_from_database(choice)
        case "exit":
            break
        case _:
            print("Please select a valid option")
