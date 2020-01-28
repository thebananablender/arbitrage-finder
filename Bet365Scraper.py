import requests
from bs4 import BeautifulSoup
from csv import writer

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
		points_Container = points_Title.find_next(class_ = "gl-MarketGroup_Wrapper")
		assists_Container = assists_Title.find_next(class_ = "gl-MarketGroup_Wrapper")
		rebounds_Container = rebounds_Title.find_next(class_ = "gl-MarketGroup_Wrapper")

		return points_Container, assists_Container, rebounds_Container

	def write_to_csv(self, points_Container, assists_Container, rebounds_Container, csv_writer):
		
		# Finds within player points market every players name, odds and points
		names = points_Container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = points_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = points_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		# Writes to csv files: names|market, Over odds, Under odds, points.
		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|P',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

		names = assists_Container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = assists_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = assists_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|A',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

		names = rebounds_Container.find_all(class_ = "srb-ParticipantLabelWithTeam_Name")
		odds = rebounds_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Odds")
		points = rebounds_Container.find_all(class_ = "gl-ParticipantCenteredStacked_Handicap")

		count = 0
		for i in range(len(odds)//2):
			csv_writer.writerow([names[i].get_text()+'|R',odds[count].get_text(),odds[len(odds)//2 + count].get_text(),points[count].get_text()])
			count += 1

		
	
