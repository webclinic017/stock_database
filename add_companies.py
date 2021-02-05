'''
author: Nicholas Brodeur

created on 2021-01-14

This file retrieves publicly traded stocks and basic information about them from the Financial Modeling Prep API and 
stores them into a SQLite database.

'''

from urllib.request import urlopen
import json

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.
    Parameters
    ----------
    url : str
    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)



import sqlite3
from fmp_stock import fmp_stock
import time

def add_to_database(ticker, api_key):	
	
	# Create a stock object
	stock = fmp_stock(ticker, api_key)

	# Pull JSON data from the FMP API
	print('\nPulling', ticker, 'profile data...')
	stock.pull_profile()

	# Enter JSON data into the database
	print('Entering into database...\n')
	sector = stock.profile[0]['sector']
	cur.execute('INSERT OR IGNORE INTO Sector (name) VALUES ( ? )', ( sector, ))
	cur.execute('SELECT id, name FROM Sector WHERE name = ? ', ( sector, ))
	sector_id = cur.fetchone()[0]

	industry = stock.profile[0]['industry']
	cur.execute('INSERT OR IGNORE INTO Industry (name, sector_id) VALUES ( ?, ? )', ( industry, sector_id ))
	cur.execute('SELECT id, name FROM Industry WHERE name = ? ', ( industry, ))
	industry_id = cur.fetchone()[0]

	exchange_short = stock.profile[0]['exchangeShortName']
	exchange = stock.profile[0]['exchange']
	cur.execute('INSERT OR IGNORE INTO Exchange (short_name, long_name) VALUES ( ?, ? )', ( exchange_short, exchange ))
	cur.execute('SELECT id, short_name FROM Exchange WHERE short_name = ? ', ( exchange_short, ))
	exchange_id = cur.fetchone()[0]

	cur.execute('''INSERT OR IGNORE INTO Company (industry_id, sector_id, exchange_id, 
		ticker, name, description, ceo, ipo_date, website) 
		VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
		(industry_id, sector_id, exchange_id, stock.ticker, stock.profile[0]['companyName'], 
			stock.profile[0]['description'], stock.profile[0]['ceo'], 
			stock.profile[0]['ipoDate'], stock.profile[0]['website']))
	cur.execute('SELECT id, ticker FROM Company WHERE ticker = ? ', ( stock.ticker, ))
	company_id = cur.fetchone()[0]

	# Commit stock to database
	conn.commit()








### MAIN CODE ###

# Open SQLite database
conn = sqlite3.connect('stocks.sqlite')
cur = conn.cursor()

# Initialize tables
cur.executescript('''
	CREATE TABLE IF NOT EXISTS Sector (
		id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		name 		TEXT UNIQUE
	);
	CREATE TABLE IF NOT EXISTS Industry (
		id 				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		sector_id		INTEGER,
		name 			TEXT UNIQUE
	);
	CREATE TABLE IF NOT EXISTS Exchange (
		id 				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		short_name 		TEXT UNIQUE,
		long_name		TEXT
	);
	CREATE TABLE IF NOT EXISTS Company (
		id				INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		industry_id		INTEGER,
		sector_id		INTEGER,
		exchange_id		INTEGER,
		ticker 			TEXT UNIQUE,
		name 			TEXT UNIQUE,
		description		TEXT,
		ceo 			TEXT,
		ipo_date		TEXT,
		website			TEXT
	);
''')



# Enter your FMP api key
key = "ENTER_API_KEY_HERE" 

if key == None:
	key = input('\nPlease enter your api key. \n> ')
else:
	key = "apikey=" + key

	
# Initialize a variable for ticker symbols to store FMP data for database autofill feature
symbols_json = None


while True:
	# Prompt user to add a specific stock, autofill, or quit
	ui = input('\nEnter a ticker (EX. AAPL), press enter to autofill, or type \'quit\' to quit... \n> ')


	# Autofill
	if len(ui) < 1:
		
		# Prompt user to enter the number of stocks they want to pull
		ui_stock_count = input('\nHow many stocks would you like to pull? (enter \'cancel\' to cancel) \n> ')
		if ui_stock_count == 'cancel':
			continue

		# Pull a list of ticker symbols from FMP
		if symbols_json is None:
			symbols_json = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/stock/list?' + key)
		
		# Find the first ticker symbol from FMP's list that the database hasn't logged
		start_index = 0
		while True:
			cur.execute('SELECT ticker FROM Company WHERE ticker = ? ', ( symbols_json[start_index]['symbol'], ))
			if cur.fetchone() is None:
				break
			start_index += 1
		
		
		# Initialize a list for ticker symbols
		symbols_list = []
		# Build the list starting with the first missing ticker from the FMP stock list
		for i in range(int(ui_stock_count)):
			symbols_list.append(symbols_json[i+start_index]['symbol'])

		# Loop through the ticker symbols, adding unfamiliar tickers to the database
		count = 0
		for ticker in symbols_list:
			
			# Skip stocks that are already in database; add those that aren't
			cur.execute('SELECT id FROM Company WHERE ticker = ? ', ( ticker, ))
			if cur.fetchone() is not None:
				print(ticker, 'already exists in database')
			else:
				add_to_database(ticker, key)

			# Delay program every 30 stocks
			count += 1
			if (count % 30) == 0:
				print('\nsleeping...\n')
				time.sleep(2)

	else:
		# End program
		if ui == 'quit':
			break

		# Enter user-input stock to database
		try:
			add_to_database(ui, key)
		except Exception as err:
			print('Failed to retrieve or enter', ui +'.', err)
			continue
