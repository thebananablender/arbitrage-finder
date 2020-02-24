from Collector import *

class SportsBetCollector(Collector):

	def __init__(self, url, os):
		self.url = url
		try:
			if os == 'MAC':
				opts = Options()
				opts.add_experimental_option("excludeSwitches", ["enable-automation"])
				opts.add_experimental_option('useAutomationExtension', False)
				opts.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
				opts.headless = True
				self.driver = Chrome(chrome_options=opts)
				self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
					"source": """
				    Object.defineProperty(navigator, 'webdriver', {
				      get: () => false
				    })
				  """
				})
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
			print('ERROR: Please specify either MAC or WIN in the cmd line arguments')
			return

	#Returns the URL for every game given the URL of the sport from sportsbet
	def get_games(self):
		self.driver.get(self.url)
		games = []

		for game in self.driver.find_elements_by_class_name('linkMultiMarket_fcmecz0'):
			games.append(game.get_attribute('href'))

		self.games = games

	def get_page_sources(self):
		page_sources = []

		for game in tqdm(self.games):
			#Navigate to each game
			try:
				self.driver.get(game)
			except InvalidSessionIdException:
				print("ERROR: Invalid session ID. Usually caused by attempting to scrape live games")
				continue
			try:
				# Click on 'Player Points Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Points Markets')]").click()
				points = self.driver.find_elements_by_xpath("//span[contains(text(), ' - Points')]")
				for e in points:
					e.click()
					time.sleep(.5)

				# Click on 'Player Rebounds Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Rebounds Markets')]").click()
				rebounds = self.driver.find_elements_by_xpath("//span[contains(text(), ' - Rebounds')]")
				for e in rebounds:
					e.click()
					time.sleep(.5)

				# Click on 'Player Assists Markets' accordion, and the individual player accordions
				self.driver.find_element_by_xpath("//span[contains(text(), 'Player Assists Markets')]").click()
				assists = self.driver.find_elements_by_xpath("//span[contains(text(), ' - Assists')]")
				for e in assists:
					e.click()
					time.sleep(.5)

				#append page source to return list
				page_sources.append(self.driver.page_source)
			except NoSuchElementException:
				print("ERROR: Player markets not found.")
				#close the browser window
				self.driver.close()
				continue
		self.driver.close()
			
		return page_sources



