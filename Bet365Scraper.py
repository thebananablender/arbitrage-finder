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
			if title.get_text() == "Player Points":
				points_Title = title
			if title.get_text() == "Player Assists":
				assists_Title = title
			if title.get_text() == "Player Rebounds":
				rebounds_Title = title

		points_Container = points_Title.find_next()
		assists_Container = points_Title.find_next()
		rebounds_Container = points_Title.find_next()

		return points_Container, assists_Container, rebounds_Container


	def write_to_csv(self, points_Container, assists_Container, rebounds_Container):
		with open('sportsbet_Odds.csv', 'w') as csv_file:
			csv_writer = writer(csv_file)