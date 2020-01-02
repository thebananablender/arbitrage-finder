from selenium.webdriver import Chrome
import pandas as pd

#Opens up the driver.
#Requires Chrome and ChromeDriver installed
driver = Chrome()

#Goes to sports bet
driver.get('https://www.sportsbet.com.au/betting/basketball-us/nba-matches/charlotte-hornets-at-cleveland-cavaliers-5030925')


#Market divs start at 3. 10 is an arbitrary number for now. Hopefully we can find the max number dynamically
for i in range(3, 10):
	#finds the element using xpaths. Hopefully xpaths are the same across different game pages.
	dropdown = driver.find_element_by_xpath("/html/body/span/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div/div/div/div/div/div[{}]".format(i))
	#clicks the div.
	dropdown.click()