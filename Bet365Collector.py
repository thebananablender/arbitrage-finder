from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from selenium import webdriver

#Class Retrieves page_source from Bet365 websites
class Bet365Collector:
	#Input: URL of sport
	def __init__(self, url):
		self.url = url

	#Returns a list of page_sources. Corresponding to today's games.
	def get_page_sources(self, games):
		page_sources = []

		# For macs uncomment next line and comment out windows
		# driver = Chrome() 

		# For windows uncomment next 4 lines and comment out macs
		options = webdriver.ChromeOptions()
		options.binary_location = r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe"
		chrome_driver_binary = r"/chromedriver.exe"
		driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

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

			game_page_source = self.get_game_page_source(driver)

			if(game_page_source != "Player Markets Not Found"):
				page_sources.append(game_page_source)
				driver.back()
				time.sleep(2)

			#Returns to previous page
			driver.back()
			time.sleep(2)

		return page_sources

	def get_game_page_source(self, driver):
		try:
			#Tries to find the player-market tab
			driver.find_element_by_xpath("//div[contains(text(), 'Player Markets')]").click()
			time.sleep(2)

			#Tries to ppen assists, rebounds and all show all dropdowns
			try:
				driver.find_element_by_xpath("//div[contains(text(), 'Player Assists')]").click()
				time.sleep(3)

				driver.find_element_by_xpath("//div[contains(text(), 'Player Rebounds')]").click()
				time.sleep(3)

				showMoreDropdowns = driver.find_elements_by_class_name("msl-ShowMore")
				for dropdown in showMoreDropdowns:
					dropdown.click()
					time.sleep(3)

			except NoSuchElementException:
				print("Either assist, rebound was not found. Exporting data anyway")

			#Returns the page source
			return driver.page_source

		except NoSuchElementException:
			print("Player Markets Not Found")
			return "Player Markets Not Found"