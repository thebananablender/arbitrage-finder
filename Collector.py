from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from tqdm import tqdm
import time


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