from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from selenium import webdriver
from Collector import Collector

#Class Retrieves page_source from Bet365 websites
class Bet365Collector(Collector):
	#Input: URL of sport
	def __init__(self, url, os):
		self.url = url
		try:
			if os == 'MAC':
				self.driver = Chrome()
				self.driver.implicitly_wait(10)
			elif os == 'WIN':
				options = webdriver.ChromeOptions()
				options.binary_location = r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe"
				chrome_driver_binary = r"/chromedriver.exe"
				self.driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
			else:
				raise ValueError
		except ValueError:
			print('Please specify MAC or WIN in the cmd line arguments')

	#Returns a list of page_sources. Corresponding to today's games.
	def get_games(self):
		game_urls = []
		self.driver.get(self.url)
		time.sleep(1)

		#Retrieves all game links
		games = len(self.driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText"))

		#Travels to each game
		for i in range(0, games, 2):
			self.driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText")[i].click()
			game_urls.append(self.driver.current_url)
			self.driver.back()

		self.games = game_urls

	def get_page_sources(self):
		page_sources = []
		for game in self.games:
			self.driver.get(game)
			time.sleep(1)
			try:
				#Tries to find the player-market tab
				self.driver.find_element_by_xpath("//div[contains(text(), 'Player Markets')]").click()

				#Tries to open assists, rebounds and all show all dropdowns
				try:
					self.driver.find_element_by_xpath("//div[contains(text(), 'Player Assists')]").click()
					time.sleep(1)

					self.driver.find_element_by_xpath("//div[contains(text(), 'Player Rebounds')]").click()
					time.sleep(1)

					showMoreDropdowns = self.driver.find_elements_by_class_name("msl-ShowMore")
					for dropdown in showMoreDropdowns:
						dropdown.click()
						time.sleep(1)

				except NoSuchElementException:
					print("ERROR: Either assist, rebound was not found. Exporting data anyway")

			except NoSuchElementException:
				print("ERROR: Player Markets Not Found")
				self.driver.close()
				continue

			# appends the page source
			page_sources.append(self.driver.page_source)

		self.driver.close()
		return page_sources
