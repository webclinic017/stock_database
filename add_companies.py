'''
author: Nicholas Brodeur

created on 2021-01-14

This file retrieves publicly traded stocks and basic information about them from the Financial Modeling Prep API and stores them into a SQLite database. Once the program 
is ran, the user has two options: they can enter a specific stock ticker to add/update that stock to the database, or they can press enter to randomly add a select 
number of new stocks. If you want to run this on your computer, you need to download SQLite and get an API key from https://financialmodelingprep.com/developer/docs/ . 
FMP can be used for free, but they only allow 250 calls per day, so if you are planning on making real use of their API, it is recommended that you purchase one of their
plans (unlimited requests can be purchased for only $19/mo with their monthly plan).

If you have any suggestions for improvement, I would love the feedback. Hope this is helpful!
'''

from urllib.request import urlopen
import json
import sqlite3
import time

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


# Create an api_key global variable
api_key = "ENTER_API_KEY_HERE"
api_key = "apikey=" + api_key


class fmp_stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.profile = None
        self.quote = None
        self.bal_s = None
        self.inc_s = None
        self.cf = None

    def build_url(self, retr='profile'):
        main = 'https://financialmodelingprep.com/api/v3/'
        mid = {'profile': 'profile/',
        	     'quote': 'quote/',
        	     'bal_s': 'balance-sheet-statement/', 
               'inc_s': 'income-statement/', 
               'cf': 'cash-flow-statement/'}

        if retr == 'profile' or retr == 'quote':
            return str(main+mid[retr]+self.ticker+"?"+api_key)
        elif retr == 'bal_s' or retr == 'inc_s' or retr == 'cf':
            return str(main+mid[retr]+self.ticker+"?limit=120&"+api_key)
        else:
            print("Error building url")
            return None

    def pull_profile(self):
    	self.profile = get_jsonparsed_data(self.build_url())

    def pull_quote(self):
    	self.profile = get_jsonparsed_data(self.build_url())

    def pull_finc_stmts(self):
        self.bal_s = get_jsonparsed_data(self.build_url(retr='bal_s'))
        self.inc_s = get_jsonparsed_data(self.build_url(retr='inc_s'))
        self.cf = get_jsonparsed_data(self.build_url(retr='cf')) 


def add_to_database(ticker):	
	
	# Create a stock object
	stock = fmp_stock(ticker)

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

conn = sqlite3.connect('stocks.sqlite')
cur = conn.cursor()

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

symbols_list = None

while True:
	ui = input('Enter a ticker (EX. AAPL) to add/update a specific stock to the database, press enter for database autofill, or \'quit\' to quit... ')

	if len(ui) < 1:
		
		# Pull the symbols list from FMP
		if symbols_list is None:
			symbols_list = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/stock/list?' + api_key)
		
		# Find where the code left off 
		start_index = 0
		while True:
			cur.execute('SELECT ticker FROM Company WHERE ticker = ? ', ( symbols_list[start_index]['symbol'], ))
			if cur.fetchone() is None:
				break
			start_index += 1
		
		# Ask the user how many stocks to pull
		ui_stock_count = input('\nHow many stocks would you like to pull? ')
		# Initialize a list for tickers
		tickers = []
		# Build the list starting with the first missing ticker from the FMP stock list
		for i in range(int(ui_stock_count)):
			tickers.append(symbols_list[i+start_index]['symbol'])

		# Loop through the tickers, adding unfamiliar tickers to the database
		count = 0
		for ticker in tickers:
			
			cur.execute('SELECT id FROM Company WHERE ticker = ? ', ( ticker, ))
			if cur.fetchone() is not None:
				print(ticker, 'already exists in database')
				continue
			
			add_to_database(ticker)

			# Delay program every 30 stocks to avoid overwhelming FMP servers
			if (count % 30) == 0:
				print('\nsleeping...\n')
				time.sleep(4)
			count += 1

	else:
		# End program
		if ui == 'quit':
			break

		# Attempt to add user input to database
		try:
			add_to_database(ui)
		except Exception as err:
			print('Failed to retrieve or enter', ui +'.', err)
			continue




