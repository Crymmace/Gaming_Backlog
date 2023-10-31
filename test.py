import requests
import selectorlib


URL = "https://www.metacritic.com/game/god-of-war-ragnarok"
HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, game):
        response = requests.get(URL, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("metacritic.yaml")
        value = extractor.extract(source)["score"]
        return value


event = Event()
scraped = event.scrape(URL)
extracted = event.extract(scraped)
print(extracted)
