import csv
import psycopg2
from config import config


"""
For demo purposes the database only has 5 stocks. But you can use the stock_universe.csv file to populate the database with over 3,000 stocks.
"""

def populate_stocks():
    connection = None
    insert_stock = "INSERT INTO stock(symbol, name, exchange, market_cap, sector) VALUES(%s, %s, %s, %s, %s)"

    try:
        params= config()
        print('Connecting to the PostgresSQL database...')
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        #Reading csv with stocks 
        with open('data/stocks.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            count = 0
            for row in csv_reader:
                if count == 0:
                    print("Reading stock csv rows --- Skipping header row")
                    count +=1
                if row['Market Capitalization'] != '' and row['Sector'] != '':
                    print(f"{count}. --- {row['Ticker']} --- Added.")
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