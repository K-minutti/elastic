from psaw import PushshiftAPI
import datetime
import config
import psycopg2
import psycopg2.extras

api = PushshiftAPI()

def populate_reddit():
    connection = None
    try:
        params= config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cursor.execute("SELECT * from stock")
        tickers = cursor.fetchall()

        stocks = {}
        for row in tickers:
            stocks['$' + row['symbol']] = row['id']

        #SQL to execute for each reddit post
        insert_mention = "INSERT INTO reddit(stock_id, date, content, subreddit) VALUES(%s, %s, %s, %s)"
                

        start_epoch = int(datetime.datetime(2021,4,15).timestamp())
        subs = list(api.search_submissions(after=start_epoch, 
                                        subreddit='wallstreetbets',
                                        filter=['url', 'author', 'title', 'subreddit'],
                                        limit=30))

        for sub in subs:
            words_in_title = sub.title.split()
            stock_mentions = list(set(filter(lambda word : word.lower().startswith('$'), words_in_title))) 
            if len(stock_mentions) > 0:
                for stock_mention in stock_mentions:
                    if stock_mention in stocks:
                        submit_time = datetime.datetime.fromtimestamp(sub.created_utc).isoformat()
                        try: 
                            cursor.execute(insert_mention, (stocks[stock_mention], submit_time, sub.title, 'wallstreetbets'))
                        except(Exception) as error:
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
    populate_reddit()


