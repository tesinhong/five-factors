from pandas_datareader import data as pdr                                                
import yfinance as yf
yf.pdr_override() # <== that's all it takes :-) 
symbol_AAPL = 'AAPL'
df_AAPL = pdr.get_data_yahoo(symbol_AAPL, start="2021-01-01", end="2021-09-30")
import datetime
df_AAPL.to_csv("df_price_AAPL_{}_old_data.csv".format(datetime.date.today()),index = True)
