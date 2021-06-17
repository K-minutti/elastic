import streamlit as st
from api import get_price_data

st.title("Elastic App")

st.sidebar.write("Pick your stock, industry, commodity, or crypto")

st.header("Just testing and flexing whats good")

st.write("Hey how are you doing?")

price_data = get_price_data("NOVN")
st.write(price_data)