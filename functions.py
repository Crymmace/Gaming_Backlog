from howlongtobeatpy import HowLongToBeat
from database import Database
import requests
import selectorlib

database = Database("backlog.db")


# Grabs database information.
def get_games():
    games = []
    data = database.view()
    for item in data:
        temp = ""
        for column in item:
            temp += f"{str(column)} "
        games.append(temp)
    return games


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
    game = game.replace(".", " ").replace("'", "").replace("ö", "o").replace(":", "")
    print(game)
    url = f"https://www.metacritic.com/search/{game}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    source = response.text
    extractor = selectorlib.Extractor.from_yaml_file("metacritic.yaml")
    value = extractor.extract(source)["score"][0]
    print(value)
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
