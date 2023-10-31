from howlongtobeatpy import HowLongToBeat
from database import Database
import requests
import selectorlib
import re

database = Database("backlog.db")


def find_game(game):
    games = []
    web = []
    time = []
    results = HowLongToBeat(0.0).search(game, similarity_case_sensitive=False)

    for title in results:
        games.append(title.game_name)

    for url in results:
        web.append(url.game_web_link)

    for i in results:
        time.append(i.main_story)

    i = 1
    for item in games:
        print(f"{i}. {item}")
        i += 1

    select_game(games, web, time)


def select_game(games, web, time):
    choice = int(input("Which game would you like? "))
    game_selection = games[choice - 1]
    web_selection = web[choice - 1]
    time_selection = time[choice - 1]
    print(game_selection)
    calculate_fun_quotient(get_metacritic_score(game_selection), time_selection)
    database.insert(game_selection, get_genre(web_selection), get_metacritic_score(game_selection),
                    calculate_fun_quotient(get_metacritic_score(game_selection), time_selection),
                    time_selection)


def get_games():
    data = database.view()
    print(data)


def get_genre(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    source = response.text
    extractor = selectorlib.Extractor.from_yaml_file("howlongtobeat.yaml")
    value = extractor.extract(source)["genre"]
    # To accommodate for games that have multiple divs with the same name and/or multiple genres.
    for i in value:
        if "Genre s" in i:
            return i[10:]
        elif "Genre" in i:
            return i[8:]


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


def calculate_fun_quotient(rating, time):
    fun_quotient = rating/time
    return fun_quotient


game_title = input("Enter game: ")
find_game(game_title)
get_games()
