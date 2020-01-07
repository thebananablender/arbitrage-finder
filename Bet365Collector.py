from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time



class Bet365Collector:

	def __init__(self, url):
		self.url = url

	def get_page_sources(self, games):
		page_sources = []
		driver = Chrome()
		driver.get(self.url)

		print(driver.page_source)

		game = driver.find_element_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText")
		game[0].click()


collector = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/")
games = collector.get_page_sources(collector.url)


#sl-CouponParticipantGameLineTwoWay_Name