import datetime
import time
from pygooglenews import GoogleNews
from newspaper import Article
gn = GoogleNews()


stocks = ["TWTR","TSLA","PLTR","SNOW"]
today = datetime.datetime.today().isoformat()
lookback = datetime.datetime(2021,4,15).isoformat()


for stock in stocks:
    try:
        search = gn.search(f'STOCK:{stock}', from_=lookback, to_=today)
        for entry in search['entries']:
            try:
                url= entry['link']
                article = Article(url) 
                article.download()
            except Exception as error:
                print("Cannot download article---", error)
                continue
            article.parse()
            publish_date = time.strftime('%Y-%m-%dT%H:%M:%SZ',  entry['published_parsed'])
            print("---------------------------------------------------------------------")
            print("---------------------------------------------------------------------")
            print(stock)
            print(entry['title'], "---------", publish_date)
            print("---------------------------------------------------------------------")
            print(article.text)
            print("---------------------------------------------------------------------")
            print(entry['source']['title'])
    except Exception as error:
        print(error)
