# stock_database
This code can be used to build a database of publicly traded stocks including relevant quarterly financial information using the Financial Modeling Prep API (https://financialmodelingprep.com/developer/docs/). The database can be used to collect a significant amount financial information in one location, and can be particularly useful for value investing (one example of something you could do is calculate earnings power value (EPV) for every stock and filter for the highest results to use as a lead generator for potentially excellent investments).

The Financial Modeling Prep API is free to use, but they only allow 250 requests per day for testing and debugging. If you are planning on using this code as a tool, it recommended you purchase unlimited access for $15-$19/month. (Pay for FMP here: https://financialmodelingprep.com/developer/docs/pricing)

In addition, I used SQLite as the DBMS, which means it's free and very lightweight and easy to use; However, SQLite is designed for only one user and can be cause issues if you are looking to build out/expand the database. (Download SQLite here: https://sqlite.org/download.html)


HOW TO USE:
  > RUN the add_companies.py file... 
  This builds the foundation of your database—you can add specific stocks by typing in the ticker symbol or you can set it to autofill.
  You can also run this file anytime to add more companies. 
  IMPORTANT: If you are using the free version of FMP's API, each stock you enter to the database uses 1 request (plus 1 request to autofill if you use it).
    
  > RUN the pull_financials.py file... 
    This file looks for a stock/stocks that currently exist in your database and pulls relevant financial information for them from 10Q's released over the past 5 years.
    If your database doesn't have stocks in it, or if every stock already has financial info, run the add_companies.py file to add more companies.
    Also, similar to add_companies.py, can pull financial info for specific stocks by typing in the ticker symbol or you can set it to autofill.
    IMPORTANT: If you are using the free version of FMP's API, each stock you pull financial info for uses 4 requests (use wisely!).
    
  > OPEN your SQLite DB file (it should be called 'stocks.sqlite')
