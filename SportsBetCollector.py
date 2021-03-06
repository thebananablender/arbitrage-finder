from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
from Collector import Collector

class SportsBetCollector(Collector):

	def __init__(self, url, os):
		self.url = url
		try:
			if os == 'MAC':
				self.driver = Chrome()
				self.driver.implicitly_wait(10)
				self.wait = WebDriverWait(self.driver, 10)
			elif os == 'WIN':
				options = webdriver.ChromeOptions()
				options.binary_location = r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe"
				chrome_driver_binary = r"/chromedriver.exe"
				self.driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
			else:
				raise ValueError
		except ValueError:
			print('ERROR: Please specify either MAC or WIN in the cmd line arguments')
			return

	#Returns the URL for every game given the URL of the sport from sportsbet
	def get_games(self):
		req = Request(self.url, headers = {'User-Agent': 'Mozilla/5.0'})
		html_page = urlopen(req)
		soup = BeautifulSoup(html_page, "html.parser")
		games = []

		for game in soup.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-competition-event-card')}):
			games.append('https://www.sportsbet.com.au' + game.find('a').get('href'))

		self.games = games

	def get_page_sources(self):
		page_sources = []

		for game in self.games:

			#Navigate to each game
			self.driver.get(game)
			try:
				#Click on 'Player Points Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Points Markets')]").click()
				points_container = self.get_container(self.driver, '- Points')
				points = self.get_markets(points_container, '- Points')
				for e in points:
					e.click()
					self.wait.until(lambda e: e.find_element_by_xpath(".//div[@data-automation-id='accordion-content']/div").text != "")
					time.sleep(.3)

				#Click on 'Player Rebounds Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Rebounds Markets')]").click()
				rebounds_container = self.get_container(self.driver, '- Rebounds')
				rebounds = self.get_markets(rebounds_container, '- Rebounds')
				for e in rebounds:
					e.click()
					self.wait.until(lambda e: e.find_element_by_xpath(".//div[@data-automation-id='accordion-content']/div").text != "")
					time.sleep(.3)

				#Click on 'Player Assists Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Assists Markets')]").click()
				assists_container = self.get_container(self.driver, '- Assists')
				assists = self.get_markets(assists_container, '- Assists')
				for e in assists:
					e.click()
					self.wait.until(lambda e: e.find_element_by_xpath(".//div[@data-automation-id='accordion-content']/div").text != "")
					time.sleep(.3)

				#print page source to stdout
				page_sources.append(self.driver.page_source)
			except NoSuchElementException:
				print("ERROR: Player markets not found.")
				#close the browser window
				self.driver.close()
				continue
		self.driver.close()
			
		return page_sources

	def get_markets(self, container, type):
		market = []
		items = container.find_elements_by_xpath(".//div[starts-with(@class, 'accordionItemDesktop')]")
		for item in items:
			if type in item.text:
				market.append(item)

		return market

	def get_container(self, driver, type):
		time.sleep(1)
		markets = driver.find_elements_by_xpath("//div[@data-automation-id='market-group-accordion-container']")
		for market in markets:
			if type in market.text:
				return market
		return False




