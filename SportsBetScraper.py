from bs4 import BeautifulSoup
from Scraper import Scraper


class SportsBetScraper(Scraper):

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self,source):

		soup = BeautifulSoup(source, 'html.parser')

		# Get all main market titles
		# game_name = soup.find("span", {"data-automation-id":"event-participant-1"}).get_text() + ' vs. ' + soup.find("span", {"data-automation-id":"event-participant-2"}).get_text()

		titles = soup.find_all("span",{"data-automation-id":"market-group-accordion-header-title"})

		for title in titles:
			if title.get_text() == "Player Points Markets":
				points_Title = title
			if title.get_text() == "Player Assists Markets":
				assists_Title = title
			if title.get_text() == "Player Rebounds Markets":
				rebounds_Title = title

		self.points_container = points_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})
		self.assists_container = assists_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})
		self.rebounds_container = rebounds_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})


	def write_to_csv(self, csv_writer):
		# From the container get all the names, odds and points container
		names = self.points_container.find_all("span",{"data-automation-id":"accordion-header-title"})
		odds = self.points_container.find_all("span",{"data-automation-id":"price-text"})
		points = self.points_container.find_all("span",{"class":"size12_fq5j3k2"})

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|P',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
			count += 2
		
		names = self.assists_container.find_all("span",{"data-automation-id":"accordion-header-title"})
		odds = self.assists_container.find_all("span",{"data-automation-id":"price-text"})
		points = self.assists_container.find_all("span",{"class":"size12_fq5j3k2"})

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|A',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
			count += 2
			
		names = self.rebounds_container.find_all("span",{"data-automation-id":"accordion-header-title"})
		odds = self.rebounds_container.find_all("span",{"data-automation-id":"price-text"})
		points = self.rebounds_container.find_all("span",{"class":"size12_fq5j3k2"})

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|R',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
			count += 2

	def write_to_json(self, game_name):

		#initialize the json and different markets lists
		game_json = {'game': game_name}
		points_markets = []
		assists_markets = []
		rebounds_markets = []

		#For each points market, make a market dictionary and fill in the data. At the end, append the dictionary to the points_markets array
		for tile in self.points_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			market = {}
			name = tile.find('span', {'data-automation-id':'accordion-header-title'}, text=lambda x: x and x.endswith('- Points'))
			if name is not None:
				market['player'] = name.get_text().rpartition('-')[0][:-1]
			odds = tile.find_all("span",{"data-automation-id":"price-text"})
			if odds:
				market['odds'] = [odds[0].get_text(), odds[1].get_text()]
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				market['points'] = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
			if market:
				points_markets.append(market)

		#For each assists market, make a market dictionary and fill in the data. At the end, append the dictionary to the assists_markets array
		for tile in self.assists_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			market = {}
			name = tile.find('span', {'data-automation-id':'accordion-header-title'},text=lambda x: x and x.endswith('- Assists'))
			if name is not None:
				market['player'] = name.get_text().rpartition('-')[0][:-1]
			odds = tile.find_all("span",{"data-automation-id":"price-text"})
			if odds:
				market['odds'] = [odds[0].get_text(), odds[1].get_text()]
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				market['points'] = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
			if market:
				assists_markets.append(market)

		#For each rebounds market, make a market dictionary and fill in the data. At the end, append the dictionary to the rebounds_markets array
		for tile in self.rebounds_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			market = {}
			name = tile.find('span', {'data-automation-id':'accordion-header-title'},text=lambda x: x and x.endswith('- Rebounds'))
			if name is not None:
				market['player'] = name.get_text().rpartition('-')[0][:-1]
			odds = tile.find_all("span",{"data-automation-id":"price-text"})
			if odds:
				market['odds'] = [odds[0].get_text(), odds[1].get_text()]
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				market['points'] = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
			if market:
				rebounds_markets.append(market)

		#Populate the dictionary with the *_markets arrays
		game_json['points_markets'] = points_markets
		game_json['assists_markets'] = assists_markets
		game_json['rebounds_markets'] = rebounds_markets
		
		return game_json
