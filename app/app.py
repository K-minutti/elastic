import streamlit as st
import json
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from api import get_price_data, get_stocks

st.set_page_config(layout="wide")
st.sidebar.title("elastic")
st.beta_expander('Expander')
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
st.write(f"{stock['exchange']} : {stock['symbol']}  | Sector: {stock['sector']}")

price_data_hour = symbol_data['price_data_hour']
hourly_price_data = pd.json_normalize(price_data_hour)
hr_df = hourly_price_data.iloc[::-1]
hr_df['date'] = hr_df['date'].map(lambda date: pd.Timestamp(date))

new_dates = []
unique_dates = hr_df['date'].unique().tolist()
dates = hr_df['date'].tolist()
for unique_date in unique_dates:
    date_hour_set = []
    for date in dates:
        if date == pd.Timestamp(unique_date):
            date_hour_set.append(date)
    for i, p_date in enumerate(date_hour_set):
        updated_date = p_date + datetime.timedelta(hours=i+4)
        new_dates.append(updated_date)
hr_df['hourdate'] = new_dates
            

news_score_by_date = {'date': [], 'score': []}
for date in symbol_data['news_sentiment']:
    news_score_by_date['date'].append(date)
    score = 0
    for analysis in symbol_data['news_sentiment'][date]:
        score += analysis['sentiment']
    news_score_by_date['score'].append(score)

news_sentiment = pd.DataFrame.from_dict(news_score_by_date)
news_sentiment['date'] = news_sentiment['date'].map(lambda date: pd.Timestamp(date))
ns_y_plot = []
#news_sentiment['y-plot'] =  #the price of the first row where the two dates match

st.dataframe(news_sentiment)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
               vertical_spacing=0.03, subplot_titles=(stock['name'], 'Volume'), 
               row_width=[0.2, 0.7])

fig.add_trace(go.Candlestick(x=hr_df['hourdate'], 
                            open=hr_df['open'], high=hr_df['high'],
                            low=hr_df['low'], close=hr_df['close'], name="HOURLY OHLC"
), row=1, col=1)

fig.add_trace(go.Scatter(mode="markers", x=news_sentiment['date'], y=, name='news sentiment'), row=1, col=1)

fig.add_trace(go.Bar(x=hr_df['hourdate'], y=hr_df['volume'], showlegend=False), row=2,col=1)

fig.update_layout(yaxis_title="Price", height=700, width=1250)
fig.update_layout(   paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(showgrid=False, 
        rangeslider_visible=False,
        rangebreaks=[
            dict(bounds=["sat", "mon"]),  
            dict(bounds=[20, 4], pattern="hour"),  
        ]
)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255, 255, 255, 0.5)')



#fig.add_trace(x=df['col'], y=df['col'], line=dict(color:"#fff"), name="Down up")
st.plotly_chart(fig, height=700, width=1250)


