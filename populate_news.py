import datetime
import time
from config import config
import psycopg2
import psycopg2.extras
from pygooglenews import GoogleNews
from newspaper import Article
gn = GoogleNews()



def populate_news():
    connection = None
    try:
        params= config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT * from stock")
        tickers = cursor.fetchall()

        stocks = {}
        for row in tickers:
            stocks[row['symbol']] = row['id']

        #SQL to execute for each news article
        insert_news = "INSERT INTO news(stock_id, date, title, content, source) VALUES(%s, %s, %s, %s, %s)"

        today = datetime.datetime.today().isoformat()
        lookback = datetime.datetime(2021,4,15).isoformat()
        for symbol in stocks:
            try:
                search = gn.search(f"STOCK:{symbol}", from_=lookback, to_=today)
                for entry in search['entries']:
                    try:
                        url= entry['link']
                        article = Article(url) 
                        article.download()
                    except Exception as error:
                        print("Cannot download article---")
                        print(error)
                        continue
                    article.parse()
                    publish_date = time.strftime('%Y-%m-%dT%H:%M:%SZ',  entry['published_parsed'])
                    cursor.execute(insert_news, (stocks[symbol], publish_date, entry['title'], article.text, entry['source']['title']))
            except Exception as error:
                print(error)            
        connection.commit()
        cursor.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        connection.rollback()
    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')

if __name__ == '__main__':
    populate_news()

