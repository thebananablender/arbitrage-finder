from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import time

driver = Chrome()

def getGames(url):
    req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "html.parser")
    games = []

    for game in soup.find_all('div', attrs={'data-automation-id': lambda x: x and x.endswith('-competition-event-card')}):
        games.append('https://www.sportsbet.com.au' + game.find('a').get('href'))
        # print(game.find('a').get('href'))
    return games


games = getGames("https://www.sportsbet.com.au/betting/basketball-us/nba-matches/")

for game in games:
	driver.get(game)
	# accordions = driver.find_elements_by_xpath('//div[@data-automation-id="market-group-accordion-container"]')
	driver.find_element_by_xpath("//span[contains(text(), 'Player Points Markets')]").click()
	time.sleep(1)
	points = driver.find_elements_by_xpath("//span[contains(text(), ' - Points')]")
	for e in points:
		e.click()
		time.sleep(1)

	driver.find_element_by_xpath("//span[contains(text(), 'Player Rebounds Markets')]").click()
	time.sleep(1)
	rebounds = driver.find_elements_by_xpath("//span[contains(text(), ' - Rebounds')]")
	for e in rebounds:
		e.click()
		time.sleep(1)

	driver.find_element_by_xpath("//span[contains(text(), 'Player Assists Markets')]").click()
	time.sleep(1)
	assists = driver.find_elements_by_xpath("//span[contains(text(), ' - Assists')]")
	for e in assists:
		e.click()
		time.sleep(1)

	print(driver.page_source)

driver.close()

