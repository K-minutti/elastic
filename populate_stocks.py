import csv
import psycopg2
from config import config

def populate_stocks():
    connection = None
    insert_stock = "INSERT INTO stock(symbol, name, exchange, market_cap, sector) VALUES(%s, %s, %s, %s, %s)"

    with open('data/sp500.csv') as f:
        sp500_tickers = [line.rstrip('\n') for line in f]   

    try:
        params= config()
        print('Connecting to the PostgresSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        #Reading csv with stock universe 
        with open('data/stock_universe.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            count = 0
            for row in csv_reader:
                if count == 0:
                    print("Reading stock csv rows")
                    count +=1
                if row['Market Capitalization'] == '' or row['Sector'] == '':
                    count += 1
                    continue
                if row['Ticker'] in sp500_tickers:
                    print(f"{count}. --- {row['Ticker']}--- Added.")
                    cursor.execute(insert_stock, (row['Ticker'], row['Description'], row['Exchange'], row['Market Capitalization'], row['Sector']))
                    count += 1
        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    populate_stocks()