from abc import ABC, abstractmethod

class Scraper(ABC):

    #Instantiate the collector with the base URL for selenium, and whether it is running on WIN or MAC
    @abstractmethod
    def __init__(self, sources):
        pass

    #Get a list of game urls and store it in self.games
    @abstractmethod
    def scrape_data(self, source):
        pass

    #Return the html source for each game
    @abstractmethod
    def write_to_csv(self, csv_writer):
        pass