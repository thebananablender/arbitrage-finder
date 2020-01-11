import requests
from bs4 import BeautifulSoup
from csv import writer

class Bet365Scraper:

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self, source):
		soup = BeautifulSoup(source, 'html.parser')
		