import fastapi
import uvicorn
import psycopg2
import psycopg2.extras
from config import config

api = fastapi.FastAPI()
params= config()
connection = psycopg2.connect(**params)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

@api.get('/')
def index():
    return {"messsage": "You hit elastics base url"}

@api.get('/api/stocks')
def get_stocks():
    cursor.execute(""" 
        SELECT symbol, name, exchange, market_cap, sector FROM stock ORDER BY symbol
    """)
    all_stocks = cursor.fetchall()
    stocks = {}
    for stock in all_stocks:
        stocks[stock['symbol']] = {"name" : stock['name'], "exhange" : stock['exchange'], 'market_cap': stock['market_cap'], 'sector': stock['sector']}
    return {"stocks": stocks}

@api.get('/api/sentiment')
def get_sentiment_by_symbol(symbol: str):
    cursor.execute(""" 
        SELECT * FROM stock where symbol = %s;
    """, (symbol,))
    stock_data = cursor.fetchone()
    #from price data return two sets of data one for the hourly series and another for daily
    #from news and reddit get all of the rows of data and then join for new with expert_ai_news and for reddit expert_ai_reddit
    #return a series of data for each
    print(stock_data['id'])
    return {"stock_info": stock_data}



uvicorn.run(api, host="127.0.0.1", port=8000)
