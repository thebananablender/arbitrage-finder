from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time
import threading 

class SportsBetCollector:

	def __init__(self, url):
		self.url = url

	#Returns the URL for every game given the URL of the sport from sportsbet
	def get_games(self, url):
		req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
		html_page = urlopen(req)
		soup = BeautifulSoup(html_page, "html.parser")
		games = []

		for game in soup.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-competition-event-card')}):
			games.append('https://www.sportsbet.com.au' + game.find('a').get('href'))

		return games

	def open_chrome(self):
		# For MacUser uncomment next line and comment out windows
		# driver = Chrome() 

		# For Windows uncomment next 4 lines and comment out macs
		options = webdriver.ChromeOptions()
		options.binary_location = r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe"
		chrome_driver_binary = r"/chromedriver.exe"
		driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)

		return driver

	def run_selniumn(self,game,page_sources):
		driver = self.open_chrome()
		#Navigate to each game
		driver.get(game)
		try:
			#Click on 'Player Points Markets' accordion, and the individual player accordions
			driver.find_element_by_xpath("//span[contains(text(), 'Player Points Markets')]").click()
			time.sleep(1)
			points = driver.find_elements_by_xpath("//span[contains(text(), ' - Points')]")
			for e in points:
				e.click()
				time.sleep(1)

			#Click on 'Player Rebounds Markets' accordion, and the individual player accordions
			driver.find_element_by_xpath("//span[contains(text(), 'Player Rebounds Markets')]").click()
			time.sleep(1)
			rebounds = driver.find_elements_by_xpath("//span[contains(text(), ' - Rebounds')]")
			for e in rebounds:
				e.click()
				time.sleep(1)

			#Click on 'Player Assists Markets' accordion, and the individual player accordions
			driver.find_element_by_xpath("//span[contains(text(), 'Player Assists Markets')]").click()
			time.sleep(1)
			assists = driver.find_elements_by_xpath("//span[contains(text(), ' - Assists')]")
			for e in assists:
				e.click()
				time.sleep(1)

			#print page source to stdout
			page_sources.append(driver.page_source)
		except NoSuchElementException:
			print("ERROR: Player markets not found.")
			#close the browser window
			driver.close()
			# continue
		driver.close()

	def get_page_sources(self, games):

		page_sources = []
		thread_list = []

		for game in games:
			thread = threading.Thread(target=self.run_selniumn, args=(game,page_sources,))
			thread_list.append(thread)

		for thread in thread_list:
			thread.start()

		for thread in thread_list:
			thread.join()

		return page_sources