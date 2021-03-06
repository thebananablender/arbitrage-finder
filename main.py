from SportsBetCollector import SportsBetCollector
from SportsBetScraper import SportsBetScraper
from Bet365Collector import Bet365Collector
from Bet365Scraper import Bet365Scraper
from ArbitageCalculator import ArbitageCalculator
from csv import writer
import time
import sys

def main():

	try:
		SportBet_Source = SportsBetCollector("http://www.sportsbet.com.au/betting/basketball-us/nba-matches/", sys.argv[1])
	except IndexError:
		print("ERROR: No OS argument provided.")
		return

	SportBet_Source.get_games()
	SportBet_Scraper = SportsBetScraper(SportBet_Source.get_page_sources())

	with open('sportsbet_Odds.csv','w') as sportsbet_csv_file:
		sportsbet_csv_writer = writer(sportsbet_csv_file)

		try:
			for source in SportBet_Scraper.sources:
				SportBet_Scraper.scrape_data(source)
				SportBet_Scraper.write_to_csv(sportsbet_csv_writer)
		except TypeError:
			return

	try:
		Bet365_Source = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/", sys.argv[1])
	except IndexError:
		print("ERROR: No OS argument provided.")
		return

	Bet365_Source.get_games()
	Bet365_Scraper = Bet365Scraper(Bet365_Source.get_page_sources())

	with open('bet365_Odds.csv','w') as Bet365_csv_file:
		Bet365_csv_writer = writer(Bet365_csv_file)

		try:
			for source in Bet365_Scraper.sources:
				Bet365_Scraper.scrape_data(source)
				Bet365_Scraper.write_to_csv(Bet365_csv_writer)
		except TypeError:
			return

	calc = ArbitageCalculator()
	calc.lets_go_csv()

if __name__ == "__main__":
	main()

