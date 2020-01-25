from SportsBetCollector import SportsBetCollector
from SportsBetScraper import SportsBetScraper

if __name__ == "__main__":

	collector = SportsBetCollector("https://www.sportsbet.com.au/betting/basketball-us/nba-matches/")
	games = collector.get_games(collector.url)
	scraper = SportsBetScraper(collector.get_page_sources(games))
	
	for source in scraper.sources:
		name, points, assists, rebounds = scraper.scrape_data(source)
		scraper.write_to_csv(points, assists, rebounds)

	#TODO:
	#