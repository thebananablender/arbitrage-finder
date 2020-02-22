from Collector import *

#Class Retrieves page_source from Bet365 websites
class Bet365Collector(Collector):
	#Input: URL of sport
	def __init__(self, url, os):
		self.url = url
		try:
			if os == 'MAC':
				opts = Options()
				opts.add_argument("--disable-impl-side-painting")
				opts.add_argument("--no-sandbox")
				opts.add_experimental_option("excludeSwitches", ["enable-automation"])
				opts.add_experimental_option('useAutomationExtension', False)
				opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
				opts.headless = True
				self.driver = Chrome(chrome_options=opts)
				self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
					"source": """
				    Object.defineProperty(navigator, 'webdriver', {
				      get: () => undefined
				    })
				  """
				})
				self.driver.execute_cdp_cmd("Network.enable", {})
				self.driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browser1"}})
				self.driver.implicitly_wait(5)
				self.wait = WebDriverWait(self.driver, 5)
			elif os == 'WIN':
				options = webdriver.ChromeOptions()
				options.binary_location = r"C:\Program Files (x86)\Google\Chrome Beta\Application\chrome.exe"
				chrome_driver_binary = r"/chromedriver.exe"
				self.driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
			else:
				raise ValueError
		except ValueError:
			print('Please specify MAC or WIN in the cmd line arguments')

	#Returns a list of page_sources. Corresponding to today's games.
	def get_games(self):
		game_urls = []
		self.driver.get(self.url)
		time.sleep(1.5)

		#Retrieves all game links
		games = len(self.driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText"))

		#Travels to each game
		for i in range(0, games, 2):
			self.driver.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText")[i].click()
			game_urls.append(self.driver.current_url)
			self.driver.back()
			time.sleep(1.5)

		self.games = game_urls

	def get_page_sources(self):
		page_sources = []
		for game in self.games:
			print("-game")
			self.driver.get(game)
			time.sleep(2)
			# Tries to find the player-market tab
			try:
				self.driver.find_element_by_xpath("//div[contains(text(), 'Player Markets')]").click()
				time.sleep(2)
			except NoSuchElementException:
				print("ERROR: Player markets not found for game.")
				continue

			#Tries to open assists, rebounds and all show all dropdowns
			try:
				self.driver.find_element_by_xpath("//div[contains(text(), 'Player Assists')]").click()
				time.sleep(2)

				self.driver.find_element_by_xpath("//div[contains(text(), 'Player Rebounds')]").click()
				time.sleep(2)

				showMoreDropdowns = self.driver.find_elements_by_class_name("msl-ShowMore")
				for dropdown in showMoreDropdowns:
					dropdown.click()
					time.sleep(2)

			except NoSuchElementException:
				print("ERROR: Either assist, rebound was not found. Exporting data anyway")

			# appends the page source
			page_sources.append(self.driver.page_source)

		self.driver.close()
		return page_sources
