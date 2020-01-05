# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from csv import writer

class SportsBetScraper:

	def __init__(self, sources):
		self.sources = sources

	def scrape_data(self,source):

		soup = BeautifulSoup(source, 'html.parser')

		titles = soup.find_all("span",{"data-automation-id":"market-group-accordion-header-title"})

		for title in titles:
			if title.get_text() == "Player Points Markets":
				points_Title = title
			if title.get_text() == "Player Assists Markets":
				assists_Title = title
			if title.get_text() == "Player Rebounds Markets":
				rebounds_Title = title

		points_Container = points_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})
		assists_Container = assists_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})
		rebounds_Container = rebounds_Title.find_next("div",{"data-automation-id":"market-group-accordion-container"})

		return points_Container, assists_Container, rebounds_Container


	def write_to_csv(self, points_Container, assists_Container, rebounds_Container):
		with open('sportsbet_Odds.csv','w') as csv_file:
			csv_writer = writer(csv_file)
			# csv_writer.writerow(game_name.get_text())

			names = points_Container.find_all("span",{"data-automation-id":"accordion-header-title"})
			odds = points_Container.find_all("span",{"data-automation-id":"price-text"})
			points = points_Container.find_all("span",{"class":"size12_fq5j3k2"})

			count = 0
			for i in range(len(odds)//2):
				csv_writer.writerow([names[i].get_text()+'|P',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
				count += 2
			
			names = assists_Container.find_all("span",{"data-automation-id":"accordion-header-title"})
			odds = assists_Container.find_all("span",{"data-automation-id":"price-text"})
			points = assists_Container.find_all("span",{"class":"size12_fq5j3k2"})

			count = 0
			for i in range(len(odds)//2):
				csv_writer.writerow([names[i].get_text()+'|A',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
				count += 2
				
			names = rebounds_Container.find_all("span",{"data-automation-id":"accordion-header-title"})
			odds = rebounds_Container.find_all("span",{"data-automation-id":"price-text"})
			points = rebounds_Container.find_all("span",{"class":"size12_fq5j3k2"})

			count = 0
			for i in range(len(odds)//2):
				csv_writer.writerow([names[i].get_text()+'|R',odds[count].get_text(),odds[count + 1].get_text(),points[count].get_text()])
				count += 2
		