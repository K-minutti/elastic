import psycopg2
from config import config
import yfinance as yf
import datetime 
from pandas_datareader import data as pdr
from pandas.tseries.offsets import BDay
yf.pdr_override()


def get_price_data(symbol):
    today = datetime.datetime.today()
    lookback_date = today - BDay(50)
    try:
        two_month_hourly = pdr.get_data_yahoo(symbol, start=lookback_date, end=today, interval='1h', prepost = True)
        three_month_daily = pdr.get_data_yahoo(symbol, period="3mo", interval='1d')
        return (two_month_hourly, three_month_daily)
    except Exception:
        print(f'There was an error with the symbol {symbol}. No data found.')


def populate_price_data():
    connection = None
    try:
        params= config()
        print('Connecting to the PostgresSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        cursor.execute("SELECT id, symbol from stock")
        tickers = cursor.fetchall()

        #SQL to execute for each stock
        insert_price_data = "INSERT INTO price_data(stock_id, date, open, high, low, close, volume, interval) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                
        for stock in tickers:
            #getting data from yfinance
            try: 
                two_month_hourly, three_month_daily = get_price_data(stock[1])
                if two_month_hourly.empty or three_month_daily.empty:
                    continue
                #stock[0] === stock id in stock table row.Index === time series Date
                for row in two_month_hourly.itertuples(index=True):
                    cursor.execute(insert_price_data, (stock[0], row.Index, row.Open, row.High, row.Low, row.Close, row.Volume, 'hour'))

                for row in three_month_daily.itertuples(index=True):
                    cursor.execute(insert_price_data, (stock[0],  row.Index, row.Open, row.High, row.Low, row.Close, row.Volume, 'day'))
            except(Exception) as error:
                print(error)
            
        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    populate_price_data()