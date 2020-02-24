from Scraper import Scraper
from bs4 import BeautifulSoup

class SportsBetScraper(Scraper):

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self,source):

		soup = BeautifulSoup(source, 'html.parser')
		team_1 = soup.find("span", {"data-automation-id":"event-participant-1"}).get_text().split()
		team_2 = soup.find("span", {"data-automation-id":"event-participant-2"}).get_text().split()
		self.game_name = team_1[0][0]+team_1[-1][0] + ' vs. ' + team_2[0][0]+team_2[-1][0]

		self.points_container = soup.find("span", text='Player Points Markets').find_next("div",{"data-automation-id":"market-group-accordion-container"})
		self.assists_container =  soup.find("span", text='Player Assists Markets').find_next("div",{"data-automation-id":"market-group-accordion-container"})
		self.rebounds_container = soup.find("span", text='Player Rebounds Markets').find_next("div",{"data-automation-id":"market-group-accordion-container"})

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

	def write_to_json(self):

		#initialize the json and different markets lists
		game_json = {self.game_name: {}}
		points_markets = {}
		assists_markets = {}
		rebounds_markets = {}

		#For each points market, make a market dictionary and fill in the data. At the end, append the dictionary to the points_markets array
		for tile in self.points_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			name = tile.find('span', {'data-automation-id':'accordion-header-title'}, text=lambda x: x and x.endswith('- Points'))
			if name is not None:
				name = name.get_text().rpartition('-')[0][:-1]
				points_markets[name] = {}
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				points = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
				points_markets[name][points] = {}
			odds = tile.find_all("span",{"data-automation-id":"price-text"})
			if odds:
				points_markets[name][points]['over'] = {"sportsbet":odds[0].get_text()}
				points_markets[name][points]['under'] = {"sportsbet":odds[1].get_text()}

		#For each assists market, make a market dictionary and fill in the data. At the end, append the dictionary to the assists_markets array
		for tile in self.assists_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			name = tile.find('span', {'data-automation-id':'accordion-header-title'},text=lambda x: x and x.endswith('- Assists'))
			if name is not None:
				name = name.get_text().rpartition('-')[0][:-1]
				assists_markets[name] = {}
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				points = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
				assists_markets[name][points] = {}
			odds = tile.find_all("span", {"data-automation-id": "price-text"})
			if odds:
				assists_markets[name][points]['over'] = {"sportsbet":odds[0].get_text()}
				assists_markets[name][points]['under'] = {"sportsbet":odds[1].get_text()}

		#For each rebounds market, make a market dictionary and fill in the data. At the end, append the dictionary to the rebounds_markets array
		for tile in self.rebounds_container.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-market-item')}):
			name = tile.find('span', {'data-automation-id':'accordion-header-title'},text=lambda x: x and x.endswith('- Rebounds'))
			if name is not None:
				name = name.get_text().rpartition('-')[0][:-1]
				rebounds_markets[name] = {}
			points = tile.find("span", {"data-automation-id": lambda x: x and x.endswith('-two-outcome-outcome-name')})
			if points is not None:
				points = ''.join(c for c in points.get_text() if c.isdigit() or c == '.')
				rebounds_markets[name][points] = {}
			odds = tile.find_all("span", {"data-automation-id": "price-text"})
			if odds:
				rebounds_markets[name][points]['over'] = {"sportsbet":odds[0].get_text()}
				rebounds_markets[name][points]['under'] = {"sportsbet":odds[1].get_text()}

		#Populate the dictionary with the *_markets arrays
		game_json[self.game_name]['points_markets'] = points_markets
		game_json[self.game_name]['assists_markets'] = assists_markets
		game_json[self.game_name]['rebounds_markets'] = rebounds_markets

		return game_json
