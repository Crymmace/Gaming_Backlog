from howlongtobeatpy import HowLongToBeat
from database import Database
import requests
import selectorlib

database = Database("backlog.db")


# Grabs database information.
def get_games():
    data = database.view()
    print(data)


# Searches for game titles based on user input.
def find_game(game):
    results = HowLongToBeat(0.0).search(game, similarity_case_sensitive=False)
    return results


# Selects game from games list.
def game_selection(game, user_choice):
    game_choice = game[user_choice]
    return game_choice


# Selects url from web list.
def url_selection(weblink, user_choice):
    web_choice = weblink[user_choice]
    return web_choice


# Selects time from time list.
def time_selection(time_entry, user_choice):
    time_choice = time_entry[user_choice]
    return time_choice


def get_genre(web_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(web_link, headers=headers)
    source = response.text
    extractor = selectorlib.Extractor.from_yaml_file("howlongtobeat.yaml")
    values = extractor.extract(source)["genre"]
    # To accommodate for games that have multiple divs with the same name and/or multiple genres.
    for value in values:
        print(values)
        if "Genre s" in value:
            return value[10:]
        elif "Genre" in value:
            return value[8:]


def get_genre2(web_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(web_link, headers=headers)
    source = response.text
    extractor = selectorlib.Extractor.from_yaml_file("howlongtobeat2.yaml")
    values = extractor.extract(source)["genre"]
    for value in values:
        if "Genre s" in value:
            return value[10:]
        elif "Genre" in value:
            return value[8:]


def get_metacritic_score(game):
    game = str(game).lower()
    game = game.replace(" ", "-").replace("'", "").replace("ö", "o").replace(":", "")
    print(game)
    url = f"https://www.metacritic.com/game/{game}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    source = response.text
    extractor = selectorlib.Extractor.from_yaml_file("metacritic.yaml")
    value = extractor.extract(source)["score"]
    return float(value)


def calculate_fun_quotient(rate, amount_of_time):
    fun_quotient = rate/amount_of_time
    fun_quotient = 100 - fun_quotient
    return fun_quotient


def add_to_database(games_title, genre_selection, metacritic_score, fun_quotient, time_to_beat):
    database.insert(games_title, genre_selection, metacritic_score, fun_quotient,
                    time_to_beat)


def remove_from_database(selection):
    database.delete(selection)


while True:
    option = input("What would you like to do? ").lower()
    match option:
        case "add":
            game_title = input("Enter game: ")

            result = find_game(game_title)
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
            game_selection = game_selection(games, choice)
            url_selection = url_selection(web, choice)
            time_selection = time_selection(time, choice)

            # Calls get_genre functions with url_selection as the parameter and assigns value to genre variable.
            genre = get_genre(url_selection)
            if not genre:
                genre = get_genre2(url_selection)

            # Calls get_metacritic_score functions with game_selection as the parameter
            # and assigns value to rating variable.
            rating = get_metacritic_score(game_selection)

            # Calls calculate_fun_quotient function with rating and time_selection() as parameters
            # and assigns value to fun variable.
            fun = calculate_fun_quotient(rating, time_selection)

            # Adds all game information to database.
            add_to_database(game_selection, genre, rating, fun, time_selection)
        case "view":
            # Calls function to print entries currently in database.
            get_games()
        case "delete":
            get_games()
            choice = int(input("Which would you like to delete? "))
            remove_from_database(choice)
        case "exit":
            break
        case _:
            print("Please select a valid option")

