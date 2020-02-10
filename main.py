from SportsBetCollector import SportsBetCollector
from SportsBetScraper import SportsBetScraper
from Bet365Collector import Bet365Collector
from Bet365Scraper import Bet365Scraper
from ArbitageCalculator import ArbitageCalculator
from csv import writer
import time
import sys

def main():

	SportBet_Source = SportsBetCollector("http://www.sportsbet.com.au/betting/basketball-us/nba-matches/")
	SportBet_Games = SportBet_Source.get_games(SportBet_Source.url)
	try:
		SportBet_Scraper = SportsBetScraper(SportBet_Source.get_page_sources(SportBet_Games,sys.argv[1]))
	except IndexError:
		print("ERROR: No OS argument provided.")
		return

	with open('sportsbet_Odds.csv','w') as sportsbet_csv_file:
		sportsbet_csv_writer = writer(sportsbet_csv_file)

		try:
			for source in SportBet_Scraper.sources:
				points, assists, rebounds = SportBet_Scraper.scrape_data(source)
				SportBet_Scraper.write_to_csv(points, assists, rebounds,sportsbet_csv_writer)
		except TypeError:
			return

	Bet365_Source = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/")
	Bet365_Games = (Bet365_Source.url)
	try:
		Bet365_Scraper = Bet365Scraper(Bet365_Source.get_page_sources(Bet365_Games,sys.argv[1]))
	except IndexError:
		print("ERROR: No OS argument provided.")
		return

	with open('bet365_Odds.csv','w') as Bet365_csv_file:
		Bet365_csv_writer = writer(Bet365_csv_file)

		try:
			for source in Bet365_Scraper.sources:
				points, assists, rebounds = Bet365_Scraper.scrape_data(source)
				Bet365_Scraper.write_to_csv(points, assists, rebounds,Bet365_csv_writer)
		except TypeError:
			return

	calc = ArbitageCalculator()
	calc.lets_go_csv()

if __name__ == "__main__":
	main()

