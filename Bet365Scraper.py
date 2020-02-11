
from bs4 import BeautifulSoup

class Bet365Scraper:

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self, source):
		
		soup = BeautifulSoup(source, 'html.parser')
		
		game_name = soup.find(class_ = "cl-BreadcrumbDropdown")

		# Gets all market titles
		titles = soup.find_all(class_ = "gl-MarketGroupButton_Text")

		# Stores the respective titles to its position in the html
		for title in titles:
			if title.get_text() == "Player Points":
				points_Title = title
			if title.get_text() == "Player Assists":
				assists_Title = title
			if title.get_text() == "Player Rebounds":
				rebounds_Title = title

		# Uses the stored position to create a container for each market
		self.points_container = points_Title.find_next(class_ = "gl-MarketGroup_Wrapper")
		self.assists_container = assists_Title.find_next(class_ = "gl-MarketGroup_Wrapper")
		self.rebounds_container = rebounds_Title.find_next(class_ = "gl-MarketGroup_Wrapper")


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

		
	
