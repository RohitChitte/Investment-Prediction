import streamlit as st
import  pandas as pd

st.title("Stock Trend Prediction"   )
symbol = st.text_input("Enter Stock Ticker").upper()
print(symbol)
# symbol = input("Enter stock Ticker : ").upper()
tickers = pd.read_csv(r"Data/Static Data/EQUITY.csv")

if (symbol!=""):
    st.write(symbol)
    if not (tickers['SYMBOL'].eq(symbol)).any():
        st.write("Invalid Symbol please  refresh the page then enter correct symbol !")
        exit()
