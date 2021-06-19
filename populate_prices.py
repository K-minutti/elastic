import psycopg2
from config import config
import yfinance as yf
import time 
from pandas_datareader import data as pdr
yf.pdr_override()


def get_price_data(symbol):
    try:
        one_month = pdr.get_data_yahoo(symbol, period="1mo", interval='1h')
        five_years= pdr.get_data_yahoo(symbol, period="5y")
        # one_month= recent_data.to_dict()
        # five_years = max_data.to_dict()
        return (one_month, five_years)
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
        sp500_tickers = cursor.fetchall()
        count = 0
        batchsize = 50

        for stock in sp500_tickers:
            #getting data from yfinance
            count +=1
            if count % batchsize == 0:
                time.sleep(90)
            try: 
                one_month, five_years = get_price_data(stock[1])
                if one_month.empty:
                    continue

                #sql
                insert_price_data = "INSERT INTO price_data(stock_id, date, open, high, low, close, volume, interval) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
                
                for row in one_month.itertuples(index=True):
                    cursor.execute(insert_price_data, (stock[0], row.Index, row.Open, row.High, row.Low, row.Close, row.Volume, 'hour'))

                for row in five_years.itertuples(index=True):
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