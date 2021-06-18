from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

def get_data(symbol):
    try:
        recent_data = pdr.get_data_yahoo(symbol, period="1mo", interval='1h')
        max_data= pdr.get_data_yahoo(symbol, period="5y")
        one_month= recent_data.to_dict()
        five_years = max_data.to_dict()
        return (one_month, five_years)
    except Exception:
        print(f'There was an error with the symbol {symbol}. No data found.')


#analyst recommendations n = yf.Ticker("NOVN") n.recommendations
#Here we will call yahoo finance by ticker and 
#return the data as need for graphing 
#we will need 15 minute/1hr data if 1hr is not available we will convert 
#the 15 minute data to 1hr data 
#then we will pull data for 5years or the max available 
#we will split it into -> 6M, 1Y and 3Years 

