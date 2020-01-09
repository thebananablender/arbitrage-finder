from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

#Class Retrieves page_source from Bet365 websites
class Bet365Collector:
	#Input: URL of sport
	def __init__(self, url):
		self.url = url

	#Returns a list of page_sources. Corresponding to today's games.
	def get_page_sources(self, games):
		page_sources = []
		driver = Chrome()
		driver.get(self.url)
		time.sleep(3)

		#Retrieves all game links
		games = driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText")

		#Travels to each game
		i = 0
		while i < len(games):
			games = driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText")
			game = games[i];
			i += 2
			game.click()
			time.sleep(2)

			#Tries to find player markets
			

			driver.back()
			time.sleep(2)

		return games


collector = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/")
game = collector.get_page_sources(collector.url)


#sl-CouponParticipantGameLineTwoWay_Name