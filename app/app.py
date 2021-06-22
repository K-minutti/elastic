import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from api import get_price_data, get_stocks

st.sidebar.title("elastic")

stocks = get_stocks()
all_stocks = json.loads(stocks)
stock_list = []
for stock in all_stocks['stocks']:
    stock_list.append(stock['symbol'])

selected_stock = st.sidebar.selectbox("Stock", stock_list)


api_data = get_price_data(selected_stock)
symbol_data = json.loads(api_data)

stock = symbol_data['stock_info']

st.header(stock['name'])
st.write(f"{stock['exchange']} : {stock['symbol']}")

price_data_hour = symbol_data['price_data_hour']
hourly_price_data = pd.json_normalize(price_data_hour)
hr_df = hourly_price_data.iloc[::-1]
hr_df['date'] = hr_df['date'].map(lambda date: pd.Timestamp(date))



#grab all of the dates that are the same in the hourly_price_data
#then for convert the date to its hourly equivelant and append the neccessary hours to start at 4:30 am
#then for every following date that is the same as another in order increment its time by 1 hour
#pd.Timestamp("2012-05-01")
#Out[29]: Timestamp('2012-05-01 00:00:00')

#we want to transform the time_stamps to increment by hour

fig = go.Figure(data = [go.Candlestick(x=hr_df['date'], 
                            open=hr_df['open'], high=hr_df['high'],
                            low=hr_df['low'], close=hr_df['close']
                        )])

# fig.show()
st.plotly_chart(fig)


# st.sidebar.write("Pick your stock, industry, commodity, or crypto")

# st.header("Just testing and flexing whats good")

# st.write("Hey how are you doing?")





