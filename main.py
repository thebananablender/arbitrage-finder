from SportsBetCollector import SportsBetCollector
from SportsBetScraper import SportsBetScraper
from Bet365Collector import Bet365Collector
from Bet365Scraper import Bet365Scraper
from ArbitageCalculator import ArbitageCalculator
from csv import writer
import pickle
import sys
import json

def main():

	if sys.argv[2] == '--testing':
		games = {}
		#testing config - use pre-saved data
		sb_source = pickle.load(open('testdata/sportsbet_sources_test.pkl', 'rb'))
		sb_scraper = SportsBetScraper(sb_source)

		for source in sb_scraper.sources:
			sb_scraper.scrape_data(source)
			games.update(sb_scraper.write_to_json())

		b365_source = pickle.load(open('testdata/bet365_sources_test.pkl', 'rb'))
		b365_scraper = Bet365Scraper(b365_source)

		for source in b365_scraper.sources:
			b365_scraper.scrape_data(source)
			games = b365_scraper.write_to_json(games)

		calc = ArbitageCalculator()
		calc.calc_json(games)

	elif sys.argv[2] == '--dev':
		#development config
		games = {}
		calc = ArbitageCalculator()
		try:
			sb_source = SportsBetCollector("http://www.sportsbet.com.au/betting/basketball-us/nba-matches/", sys.argv[1])
			b365_source = Bet365Collector("https://www.bet365.com.au/#/AC/B18/C20604387/D48/E1453/F10/", sys.argv[1])
		except IndexError:
			print("ERROR: No OS argument provided.")
			return

		sb_source.get_games()
		sources = sb_source.get_page_sources()
		sb_scraper = SportsBetScraper(sources)

		for source in sb_scraper.sources:
			sb_scraper.scrape_data(source)
			games.update(sb_scraper.write_to_json())

		b365_source.get_games()
		sources = b365_source.get_page_sources()
		b365_scraper = Bet365Scraper(sources)

		for source in b365_scraper.sources:
			b365_scraper.scrape_data(source)
			games = b365_scraper.write_to_json(games)

		calc.calc_json(games)

if __name__ == "__main__":
	main()

