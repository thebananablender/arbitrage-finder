from abc import ABC, abstractmethod

class Collector(ABC):

    #Instantiate the collector with the base URL for selenium, and whether it is running on WIN or MAC
    @abstractmethod
    def __init__(self, url, os):
        pass

    #Get a list of game urls and store it in self.games
    @abstractmethod
    def get_games(self):
        pass

    #Return the html source for each game
    @abstractmethod
    def get_page_sources(self):
        pass