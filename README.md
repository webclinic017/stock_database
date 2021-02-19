# stock_database
This code can be used to build a database of public companies including relevant quarterly financial information using the Financial Modeling Prep API (https://financialmodelingprep.com/developer/docs/). Collecting uniform financial information in one location can be useful for many reasons, but the primary intended application is in large-scale, general analytics for value investing (for example, something you could do is create a calculated field for earnings power value (EPV)—after generating this info for a list of stocks and filtering for the highest results, you're returned several potential leads/investments for further research).

The Financial Modeling Prep API is free to use, but they only allow 250 requests per day for testing and debugging. If you are planning on using this code as a tool, it recommended you purchase unlimited access for $15-$19/month. (Pay for FMP here: https://financialmodelingprep.com/developer/docs/pricing)

In addition, I used SQLite as the DBMS, which means it's free and very user-friendly (especially for people with little/no experience with databases); However, SQLite is designed for only one user and can cause issues if you are looking to seriously build out/expand the database. (Download SQLite here: https://sqlite.org/download.html)


HOW TO USE:
  > DOWNLOAD add_companies.py, pull_financials.py, and SQLite DB

  > SIGN up for an account at https://financialmodelingprep.com/developer and enter your api key into the files add_companies.py and pull_financials.py

  > RUN the add_companies.py file... 
This must be run first and builds the foundation of your database—you can add specific stocks by typing in the ticker symbol or you can set it to autofill. After running for the first time, you will notice a file 'stocks.sqlite' pop up in your working directory; double-click it to open, and you should see your database. IMPORTANT: If you are using the free version of FMP's API, since each stock you enter to uses 1 request, and using the autofill feature uses 1 request, you can only add up to 249 companies/day using autofill. Check your number of remaining calls on FMP's developer site under your user dashboard.
    
  > RUN the pull_financials.py file... 
This file looks for a stock/stocks that currently exist in your database and pulls relevant financial information for them from 10Q's released over the past 5 years—similar to add_companies.py, can pull financial info for specific stocks by typing in the ticker symbol or you can set it to autofill. If every stock already has financial info, you will need to run the add_companies.py file to add more companies. IMPORTANT: If you are using the free version of FMP's API, since each stock you pull financial info for uses 3 requests, you can only pull the financials for up to 83 companies/day. Again, check your number of remaining calls on FMP's developer site under your user dashboard.
    
  > OPEN 'stocks.sqlite' from your working directory
Your database will contain general information from each company's income statement, balance sheet, and statement of cashflows; if you need information not collected in the DB to make a calculation, you can edit the SQL in the pull_financials.py file to include it. You'll have to read through FMP's JSON structure for their income statements/balance sheets/etc from their documentation so your revised files will pull the specific data you're looking for. If you want to add calculated fields, you can do so from within the SQLite browser.
