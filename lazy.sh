#!/bin/bash
rm test
python3 SportsBetScraper.py
python3 Bet365Scraper.py
g++ -o test ArbitageCalculator.cpp
./test