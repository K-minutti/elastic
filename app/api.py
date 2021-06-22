import httpx

def get_stocks():
    res = httpx.get(f'http://127.0.0.1:8000/api/stocks')
    return res.content

def get_price_data(symbol):
    res = httpx.get(f'http://127.0.0.1:8000/api/sentiment?symbol={symbol}')
    return res.content

