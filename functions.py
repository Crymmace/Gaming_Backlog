from howlongtobeatpy import HowLongToBeat
from backlog import Database
import requests
import selectorlib

database = Database("backlog.db")


# Grabs database information.
def get_games():
    games = []
    # Opens database
    data = database.view_backlog()
    for item in data:
        temp = ""
        # Takes each column, converts into a string, and adds into temp.
        for column in item:
            temp += f"{str(column)} "
        # Appends data from temp into games.
        games.append(temp)
    return games


# Searches for game titles based on user input.
def find_game(game):
    # Searches for game info using HowLongToBeat API.
    results = HowLongToBeat(0.0).search(game, similarity_case_sensitive=False)
    return results


def find_game_by_id(id_):
    result = HowLongToBeat(0.0).search_from_id(id_)
    return result


# Grabs genre of specified game from howlongtobeat
def get_genre(web_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(web_link, headers=headers)
    source = response.text
    # Points to specified yaml file.
    extractor = selectorlib.Extractor.from_yaml_file("howlongtobeat.yaml")
    values = extractor.extract(source)["genre"]
    # Returns genre(s).
    for value in values:
        if "Genre s" in value:
            return value[10:]
        elif "Genre" in value:
            return value[8:]


# Grabs genre from howlongtobeat if genre is under a differently named div.
def get_genre2(web_link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(web_link, headers=headers)
    source = response.text
    # Points to specified yaml file.
    extractor = selectorlib.Extractor.from_yaml_file("howlongtobeat2.yaml")
    values = extractor.extract(source)["genre"]
    # Returns genre(s).
    for value in values:
        if "Genre s" in value:
            return value[10:]
        elif "Genre" in value:
            return value[8:]


# Organizes items in genres.txt into alphabetical order and outputs into sorted_genres.txt.
def alphabetize_genres():
    with open("genres.txt", "rt") as file:
        lines = file.readlines()
        file.close()

    with open("sorted_genres.txt", "wt") as file2:
        file2.writelines(sorted(lines))
        file2.close()


def grab_genres():
    with open("sorted_genres.txt", "r") as file:
        return file.readlines()


# Grabs game rating from metacritic
def get_metacritic_score(game):
    game = str(game).lower()
    # Replaces some special characters to prevent errors.
    game = game.replace(".", " ").replace("'", "").replace("ö", "o").replace(":", "")
    url = f"https://www.metacritic.com/search/{game}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    source = response.text
    # Points to specified yaml file.
    extractor = selectorlib.Extractor.from_yaml_file("metacritic.yaml")
    try:
        value = extractor.extract(source)["score"][0]
        # Returns 0 if score is "tbd". Otherwise, returns score.
        if value == "tbd":
            return 0
        else:
            return float(value)
    except TypeError:
        return 0


# Generates fun quotient using game rating, time to beat, and user preference.
def calculate_fun_quotient(rate, main, extra, completionist, preference):
    if preference == "Main Story" and main != 0:
        return round(rate / main, 1)

    # If preference is extras.
    elif preference == "Main Story and Extras" and extra != 0:
        return round(rate / extra, 1)

    # If preference is completionist.
    elif preference == "Completionist" and completionist != 0:
        return round(rate / completionist, 1)


# Adds item to database.
def add_to_database(games_title, genre_selection, metacritic_score,
                    main_story, main_story_and_extras, completionist, fun_quotient):
    database.insert_backlog(games_title, genre_selection, metacritic_score,
                            main_story, main_story_and_extras, completionist, fun_quotient)


# Removes item from database.
def remove_from_database(selection):
    database.delete_backlog(selection)


def add_preference(completion, genre):
    database.insert_preference(completion, genre)


def update_preference(row, completion, genre):
    database.update_preference(row, completion, genre)


def get_preference():
    preferences = []
    # Opens database
    data = database.view_preference()
    for item in data:
        temp = ""
        # Takes each column, converts into a string, and adds into temp.
        for column in item:
            temp += f"{str(column)} "
        # Appends data from temp into preferences.
        preferences.append(temp)
    return preferences


def search_preference_genre():
    preference = []
    data = database.search_preference_genre()
    for item in data:
        preference.append(item)

    return preference


def search_preference_completion():
    return database.search_preference_completion()

