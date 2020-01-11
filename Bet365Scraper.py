import requests
from bs4 import BeautifulSoup
from csv import writer

class Bet365Scraper:

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self, source):
		
		soup = BeautifulSoup(source, 'html.parser')
		
		titles = soup.find_all("div", {"class":"gl-MarketGroupButton_Text"})

		for title in titles:
			if title.get_text() == "Player Points Markets":
				points_Title = title
			if title.get_text() == "Player Assists Markets":
				assists_Title = title
			if title.get_text() == "Player Rebounds Markets":
				rebounds_Title = title

		