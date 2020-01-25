from SportsBetCollector import SportsBetCollector
from SportsBetScraper import SportsBetScraper
from Bet365Collector import Bet365Collector
from Bet365Scraper import Bet365Scraper
from ArbitageCalculator import ArbitageCalculator
from csv import writer
import time

if __name__ == "__main__":
	SportBet_Source = SportsBetCollector("http://www.sportsbet.com.au/betting/basketball-us/nba-matches/")
	SportBet_Games = SportBet_Source.get_games(SportBet_Source.url)
	SportBet_Scraper  = SportsBetScraper(SportBet_Source.get_page_sources(SportBet_Games))

	with open('sportsbet_Odds.csv','w') as sportsbet_csv_file:
		sportsbet_csv_writer = writer(sportsbet_csv_file)

		for source in SportBet_Scraper.sources:
			points, assists, rebounds = SportBet_Scraper.scrape_data(source)
			SportBet_Scraper.write_to_csv(points, assists, rebounds,sportsbet_csv_writer)

	Bet365_Source = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/")
	Bet365_Games = (Bet365_Source.url)
	Bet365_Scraper = Bet365Scraper(Bet365_Source.get_page_sources(Bet365_Games))

	with open('bet365_Odds.csv','w') as Bet365_csv_file:
		Bet365_csv_writer = writer(Bet365_csv_file)

		for source in Bet365_Scraper.sources:
			points, assists, rebounds = Bet365_Scraper.scrape_data(source)
			Bet365_Scraper.write_to_csv(points, assists, rebounds,Bet365_csv_writer)

	calc = ArbitageCalculator()
	calc.lets_go_csv()
