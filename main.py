import uvicorn
import psycopg2
import psycopg2.extras
from config import config
from fastapi import FastAPI, Request

api = FastAPI()
params= config()
connection = psycopg2.connect(**params)
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

@api.get('/')
def index():
    return {"messsage": "You hit elastics base url"}

@api.get('/api/stocks')
def get_stocks():
    cursor.execute(""" 
        SELECT symbol FROM stock ORDER BY symbol
    """)
    all_stocks = cursor.fetchall()
    return {"stocks": all_stocks}

@api.get('/api/sentiment')
def get_sentiment_by_symbol(symbol: str, request: Request):
    cursor.execute(""" 
        SELECT * FROM stock WHERE symbol = %s;
    """, (symbol,))
    stock = cursor.fetchone()
    stock_id = stock['id']
    
    cursor.execute("""
        SELECT * FROM price_data WHERE stock_id = %s AND interval = 'hour';
    """, (stock_id,))
    hourly_price_data = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM price_data WHERE stock_id = %s AND interval = 'day';
    """, (stock_id,))
    daily_price_data = cursor.fetchall()

    cursor.execute("""
        SELECT * FROM news WHERE stock_id = %s;
    """, (stock_id,))
    news = cursor.fetchall()

    news_sentiment_by_date = {}
    for news_item in news:
        cursor.execute("""
        SELECT * FROM expert_ai_news WHERE source_id = %s;
        """, (news_item['id'],))
        article_analysis =  cursor.fetchone()
        if news_item['date'] in news_sentiment_by_date:
            news_sentiment_by_date[news_item['date']].append(article_analysis)
        else:
            news_sentiment_by_date[news_item['date']] = [article_analysis]
        

    reddit_sentiment_by_date = {}
    for reddit_post in news:
        cursor.execute("""
        SELECT * FROM expert_ai_reddit WHERE source_id = %s;
        """, (reddit_post['id'],))
        post_analysis =  cursor.fetchone()
        if reddit_post['date'] in reddit_sentiment_by_date:
            reddit_sentiment_by_date[reddit_post['date']].append(post_analysis)
        else:
            reddit_sentiment_by_date[reddit_post['date']] = [post_analysis]
        
    #http://127.0.0.1:8000/api/sentiment?symbol=TWTR
    return {"stock_info": stock,  "price_data_hour": hourly_price_data, "price_data_day": daily_price_data, "news_sentiment": news_sentiment_by_date, "reddit_sentiment":  reddit_sentiment_by_date }



uvicorn.run(api, host="127.0.0.1", port=8000)
