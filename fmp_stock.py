'''
author: Nicholas Brodeur

created on 2021-02-05

This file creates a class 'fmp_stock' that allows the user to easily pull public company profile
and financial data

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



class fmp_stock:
    def __init__(self, ticker, api_key):
        self.ticker = ticker
        self.api_key = api_key

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
            return str(main+mid[retr]+self.ticker+"?"+self.api_key)
        elif retr == 'bal_s' or retr == 'inc_s' or retr == 'cf':
            return str(main+mid[retr]+self.ticker+"?limit=120&"+self.api_key)
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
