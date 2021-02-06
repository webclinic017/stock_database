'''
author: Nicholas Brodeur

created on 2021-01-14

This file opens the database created by the add_companies.py file and adds relevant quarterly 
financial information retrieved from the Financial Modeling Prep API

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

def pull_financials(ticker, api_key):	
	
	# Create a stock object
	stock = fmp_stock(ticker, api_key)

	# Pull JSON data from the FMP API
	print('\nPulling', ticker, 'financial data...')
	stock.pull_finc_stmts()


	### Enter JSON data into the database ###
	print('Entering general 10Q info...\n')

	# General 10Q 
	company_id = []
	as_of_date = []
	period = []

	for form10Q in stock.inc_s:
		cur.execute('SELECT id FROM Company WHERE ticker = ? ', ( ticker, ))
		company_id.append(cur.fetchone()[0])
		as_of_date.append(form10Q['date'])
		period.append(form10Q['period'])

	# Income Statement
	revenue = []
	cost_of_revenue = []
	gross_profit = []
	ebitda = []
	operating_income = []
	income_before_tax = []
	net_income = []
	earnings_per_share = []
	earnings_per_share_diluted = []
	weighted_avg_shares_outstanding = []
	weighted_avg_shares_outstanding_diluted = []

	for form10Q in stock.inc_s:
		revenue.append(form10Q['revenue'])
		cost_of_revenue.append(form10Q['costOfRevenue'])
		gross_profit.append(form10Q['grossProfit'])
		ebitda.append(form10Q['ebitda'])
		operating_income.append(form10Q['operatingIncome'])
		income_before_tax.append(form10Q['incomeBeforeTax'])
		net_income.append(form10Q['netIncome'])
		earnings_per_share.append(form10Q['eps'])
		earnings_per_share_diluted.append(form10Q['epsdiluted'])
		weighted_avg_shares_outstanding.append(form10Q['weightedAverageShsOut'])
		weighted_avg_shares_outstanding_diluted.append(form10Q['weightedAverageShsOutDil'])

	# Balance Sheet
	total_current_assets = []
	total_non_current_assets = []
	other_assets = []
	total_assets = []
	total_current_liabilities = []
	total_non_current_liabilities = []
	other_liabilities = []
	total_liabilities = []
	common_stock = []
	retained_earnings = []
	total_stockholders_equity = []

	for form10Q in stock.bal_s:
		total_current_assets.append(form10Q['totalCurrentAssets'])
		total_non_current_assets.append(form10Q['totalNonCurrentAssets'])
		other_assets.append(form10Q['otherAssets'])
		total_assets.append(form10Q['totalAssets'])
		total_current_liabilities.append(form10Q['totalCurrentLiabilities'])
		total_non_current_liabilities.append(form10Q['totalNonCurrentLiabilities'])
		other_liabilities.append(form10Q['otherLiabilities'])
		total_liabilities.append(form10Q['totalLiabilities'])
		common_stock.append(form10Q['commonStock'])
		retained_earnings.append(form10Q['retainedEarnings'])
		total_stockholders_equity.append(form10Q['totalStockholdersEquity'])

	# Cash Flow
	net_cash_provided_by_operating_activities = []
	net_cash_used_for_investing_activities = []
	net_cash_used_provided_by_financing_activities = []
	net_change_in_cash = []
	cash_at_end_of_period = []
	cash_at_beginning_of_period = []
	operating_cash_flow = []
	capital_expenditure = []
	free_cash_flow = []

	for form10Q in stock.cf:
		net_cash_provided_by_operating_activities.append(form10Q['netCashProvidedByOperatingActivities'])
		net_cash_used_for_investing_activities.append(form10Q['netCashUsedForInvestingActivites'])
		net_cash_used_provided_by_financing_activities.append(form10Q['netCashUsedProvidedByFinancingActivities'])
		net_change_in_cash.append(form10Q['netChangeInCash'])
		cash_at_end_of_period.append(form10Q['cashAtEndOfPeriod'])
		cash_at_beginning_of_period.append(form10Q['cashAtBeginningOfPeriod'])
		operating_cash_flow.append(form10Q['operatingCashFlow'])
		capital_expenditure.append(form10Q['capitalExpenditure'])
		free_cash_flow.append(form10Q['freeCashFlow'])


	# Add records to database
	for i in range(len(company_id)):
		cur.execute('''INSERT OR IGNORE INTO Form10Q (company_id, as_of_date, period, revenue, 
			cost_of_revenue, gross_profit, ebitda, operating_income, income_before_tax, 
			net_income, earnings_per_share, earnings_per_share_diluted, 
			weighted_avg_shares_outstanding, weighted_avg_shares_outstanding_diluted, 
			total_current_assets, total_non_current_assets, other_assets, total_assets, 
			total_current_liabilities, total_non_current_liabilities, other_liabilities, 
			total_liabilities, common_stock, retained_earnings, total_stockholders_equity, 
			net_cash_provided_by_operating_activities, net_cash_used_for_investing_activities, 
			net_cash_used_provided_by_financing_activities, net_change_in_cash, cash_at_end_of_period, 
			cash_at_beginning_of_period, operating_cash_flow, capital_expenditure, free_cash_flow) 
			VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
			?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( company_id[i], as_of_date[i], period[i], revenue[i], 
				cost_of_revenue[i], gross_profit[i], ebitda[i], operating_income[i], income_before_tax[i], 
				net_income[i], earnings_per_share[i], earnings_per_share_diluted[i], 
				weighted_avg_shares_outstanding[i], weighted_avg_shares_outstanding_diluted[i], 
				total_current_assets[i], total_non_current_assets[i], other_assets[i], total_assets[i], 
				total_current_liabilities[i], total_non_current_liabilities[i], other_liabilities[i], 
				total_liabilities[i], common_stock[i], retained_earnings[i], total_stockholders_equity[i],
				net_cash_provided_by_operating_activities[i], net_cash_used_for_investing_activities[i], 
				net_cash_used_provided_by_financing_activities[i], net_change_in_cash[i], 
				cash_at_end_of_period[i], cash_at_beginning_of_period[i], operating_cash_flow[i], 
				capital_expenditure[i], free_cash_flow[i]))

	# Commit stock to database
	conn.commit()







### MAIN CODE ###

# Open SQLite database
conn = sqlite3.connect('stocks.sqlite')
cur = conn.cursor()

# Initialize table
cur.executescript('''
	CREATE TABLE IF NOT EXISTS Form10Q (
		id 											INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		company_id									INTEGER,
		as_of_date									TEXT,
		period										TEXT,

		revenue										INTEGER,
		cost_of_revenue								INTEGER,
		gross_profit								INTEGER,
		ebitda										INTEGER,
		operating_income							INTEGER,
		income_before_tax							INTEGER,
		net_income									INTEGER,
		earnings_per_share 							REAL,
		earnings_per_share_diluted					REAL,
		weighted_avg_shares_outstanding				INTEGER,
		weighted_avg_shares_outstanding_diluted		INTEGER,

		total_current_assets							INTEGER,
		total_non_current_assets						INTEGER,
		other_assets									INTEGER,
		total_assets									INTEGER,
		total_current_liabilities 						INTEGER,
		total_non_current_liabilities					INTEGER,
		other_liabilities								INTEGER,
		total_liabilities								INTEGER,
		common_stock									INTEGER,
		retained_earnings								INTEGER,
		total_stockholders_equity						INTEGER,

		net_cash_provided_by_operating_activities		INTEGER,
		net_cash_used_for_investing_activities			INTEGER,
		net_cash_used_provided_by_financing_activities	INTEGER,
		net_change_in_cash								INTEGER,
		cash_at_end_of_period							INTEGER,
		cash_at_beginning_of_period						INTEGER,
		operating_cash_flow								INTEGER,
		capital_expenditure								INTEGER,
		free_cash_flow									INTEGER
	);
''')




# Enter your assigned FMP api key
key = None                                        # <----- ENTER YOUR API KEY HERE 

if key == None:
	key = input('\nPlease enter your api key -> ')
key = "apikey=" + key


while True:

	# Prompt user to add a specific stock, autofill, or quit
	ui = input('\nEnter a ticker (EX. AAPL), press enter to autofill, or type \'quit\' to quit... \n> ')


	# Autofill
	if len(ui) < 1:		

		# Prompt user to enter the number of stocks they want to pull
		ui_stock_count = input('\nHow many stocks would you like to pull? (enter \'cancel\' to cancel)\n> ')
		if ui_stock_count == 'cancel':
			continue

		# Query tickers for companies where form10Q is null
		cur.execute('''SELECT ticker FROM Company LEFT JOIN Form10Q ON Company.id = Form10Q.company_id
						WHERE Form10Q.id IS NULL''')
		# Create a list of ticker symbols to pull data for
		symbols_list = cur.fetchmany(int(ui_stock_count))

		# Loop through the ticker symbols
		count = 0
		for ticker in symbols_list:
			
			# Pull info and add to database
			pull_financials(ticker[0], key)

			# Delay program every 7 stocks
			count += 1
			if (count % 7) == 0:
				print('\nsleeping...\n')
				time.sleep(2)

	else:
		# End program
		if ui == 'quit':
			break

		# Enter user-input stock to database
		try:
			pull_financials(ui, key)
		except Exception as err:
			print('Failed to pull financial data or enter into database ('+ui+').', err)
			continue
