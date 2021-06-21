import fastapi
import uvicorn
# from typing import Optional

api = fastapi.FastAPI()

@api.get('/')
def index():
    return {"messsage": "HELLLOOOO!"}

@api.get('/api/calculate')
def calculate():
    return 2 + 2

@api.get('/api/sentiment')
def get_sentiment_by_symbol(symbol: str):
    one_month, five_years = get_data(symbol)
    return {"price_data_1M": one_month}



uvicorn.run(api, host="127.0.0.1", port=8000)
