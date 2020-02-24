from Scraper import Scraper
from bs4 import BeautifulSoup

class Bet365Scraper(Scraper):

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self, source):
		
		soup = BeautifulSoup(source, 'html.parser')

		team_1 = soup.find(class_ = "cl-BreadcrumbDropdown").get_text().split('@')[0].split()
		team_2 = soup.find(class_ = "cl-BreadcrumbDropdown").get_text().split('@')[1].split()
		self.game_name =team_1[0][0]+team_1[-1][0] + ' vs. ' + team_2[0][0]+team_2[-1][0]

		# Uses the stored position to create a container for each market
		self.points_container = soup.find(class_ = "gl-MarketGroupButton_Text", text="Player Points").find_next(class_ = "gl-MarketGroup_Wrapper")
		self.assists_container = soup.find(class_ = "gl-MarketGroupButton_Text", text="Player Assists").find_next(class_ = "gl-MarketGroup_Wrapper")
		self.rebounds_container = soup.find(class_ = "gl-MarketGroupButton_Text", text="Player Rebounds").find_next(class_ = "gl-MarketGroup_Wrapper")


	def write_to_csv(self, csv_writer):
		
		# Finds within player points market every players name, odds and points
		names = self.points_container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = self.points_container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = self.points_container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		# Writes to csv files: names|market,Over odds,Under odds, points.
		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|P',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

		names = self.assists_container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = self.assists_container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = self.assists_container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|A',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

		names = self.rebounds_container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = self.rebounds_container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = self.rebounds_container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|R',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

	def write_to_json(self, games_json):
		game = games_json[self.game_name]
		points_markets = game['points_markets']
		assists_markets = game['assists_markets']
		rebounds_markets = game['rebounds_markets']

		names = self.points_container.find_all(class_="gl-Market_General-columnheader")[0].find_all(class_="srb-ParticipantLabelWithTeam_Name")
		over_odds = self.points_container.find_all(class_="gl-Market_General-columnheader")[1].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		under_odds = self.points_container.find_all(class_="gl-Market_General-columnheader")[2].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		points = self.points_container.find_all(class_="gl-ParticipantCenteredStacked_Handicap")

		for i in range(len(names)):
			name = names[i].get_text()
			if name in points_markets:
				point = points[i].get_text()
				if point in points_markets[name]:
					points_markets[name][point]['over'].update({"b365":over_odds[i].get_text()})
					points_markets[name][point]['under'].update({"b365":under_odds[i].get_text()})
				else:
					points_markets[name].update({point:{"over": {"b365":over_odds[i].get_text()}}})
					points_markets[name][point]['under'] = {"b365":under_odds[i].get_text()}
			else:
				points_markets.update({name: {}})
				point = points[i].get_text()
				points_markets[name].update({point: {"over": {"b365": over_odds[i].get_text()}}})
				points_markets[name][point]['under'] = {"b365": under_odds[i].get_text()}

		names = self.assists_container.find_all(class_="gl-Market_General-columnheader")[0].find_all(class_="srb-ParticipantLabelWithTeam_Name")
		over_odds = self.assists_container.find_all(class_="gl-Market_General-columnheader")[1].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		under_odds = self.assists_container.find_all(class_="gl-Market_General-columnheader")[2].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		points = self.assists_container.find_all(class_="gl-ParticipantCenteredStacked_Handicap")

		for i in range(len(names)):
			name = names[i].get_text()
			if name in assists_markets:
				point = points[i].get_text()
				if point in assists_markets[name]:
					assists_markets[name][point]['over'].update({"b365": over_odds[i].get_text()})
					assists_markets[name][point]['under'].update({"b365": under_odds[i].get_text()})
				else:
					assists_markets[name].update({point: {"over": {"b365": over_odds[i].get_text()}}})
					assists_markets[name][point]['under'] = {"b365": under_odds[i].get_text()}
			else:
				assists_markets.update({name: {}})
				point = points[i].get_text()
				assists_markets[name].update({point: {"over": {"b365": over_odds[i].get_text()}}})
				assists_markets[name][point]['under'] = {"b365": under_odds[i].get_text()}

		names = self.rebounds_container.find_all(class_="gl-Market_General-columnheader")[0].find_all(class_="srb-ParticipantLabelWithTeam_Name")
		over_odds = self.rebounds_container.find_all(class_="gl-Market_General-columnheader")[1].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		under_odds = self.rebounds_container.find_all(class_="gl-Market_General-columnheader")[2].find_all(class_="gl-ParticipantCenteredStacked_Odds")
		points = self.rebounds_container.find_all(class_="gl-ParticipantCenteredStacked_Handicap")

		for i in range(len(names)):
			name = names[i].get_text()
			if name in rebounds_markets:
				point = points[i].get_text()
				if point in rebounds_markets[name]:
					rebounds_markets[name][point]['over'].update({"b365": over_odds[i].get_text()})
					rebounds_markets[name][point]['under'].update({"b365": under_odds[i].get_text()})
				else:
					rebounds_markets[name].update({point: {"over": {"b365": over_odds[i].get_text()}}})
					rebounds_markets[name][point]['under'] = {"b365": under_odds[i].get_text()}
			else:
				rebounds_markets.update({name: {}})
				point = points[i].get_text()
				rebounds_markets[name].update({point: {"over": {"b365": over_odds[i].get_text()}}})
				rebounds_markets[name][point]['under'] = {"b365": under_odds[i].get_text()}

		return games_json
	
