import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from nsepy import get_history
from datetime import date
from keras.models import load_model
from pickle import load
import time
import os
import Data_Scrapping
import  testing_pipeline
import DB_Files.Cassandra_Database
import threading
from Logger.logging import App_Logger
import streamlit as st


def driver(symbol):

  data = Data_Scrapping.scrap_data_from_yahoo_finance(symbol)
  st.subheader("Data Scrapped Successfully")
  st.write(data.head(3))
  st.write(data.tail(3))
  st.subheader("Database operations started !")
  t1.start()

  filename = os.listdir("Data\Scraped Data")[0]
  st.subheader("Prediction pipeline started !")
  testing = testing_pipeline.testing_data(f"Data\Scraped Data\{filename}")

  pred = testing_pipeline.prediction(testing)
  actual_vs_predicted = pd.read_csv("Data\Scraped Data\\" + filename)[["Price", "Date"]][100:]
  # print(testing)
  actual_vs_predicted["Prediction"] = pred

  st.subheader("Predictions VS Original")

  plt.figure(figsize=(12, 6))
  plt.xticks(rotation=90)
  plt.tight_layout()
  plt.plot(actual_vs_predicted["Price"], 'b', label='Actual Price')
  plt.plot(actual_vs_predicted["Prediction"], 'r', label='Predicted Price')
  plt.xlabel('Time')
  plt.ylabel('Price')
  plt.legend()
  # plt.show()
  # Saving png file to archieve/Prediction Figures
  (os.chdir(os.getcwd()[:63]))
  path = (os.getcwd()[:63] + "\\" + f"Archieve_Files\\Prediction Figures\{os.listdir('Data/Scraped Data')[0]}"[
                                    :-4] + ".png")
  if (os.path.exists(path)):
    os.remove(path)
  plt.savefig(path)
  st.pyplot(plt)

def Db():
  DB_obj = DB_Files.Cassandra_Database.CassandraDBManagement()
  DB_obj.upload_data_to_DB('demo')
  # print(DB_obj.fetch_data_from_table_in_DB('demo'))


start = time.time()
t1 = threading.Thread(target=Db)

st.title("Stock Trend Prediction")
symbol = st.text_input("Enter Stock Ticker").upper()
# symbol = input("Enter stock Ticker : ").upper()

if(symbol!=""):
  tickers = pd.read_csv(r"Data/Static Data/EQUITY.csv")

  if ((symbol!='NIFTY') and (symbol!="BANKNIFTY")):
    if not(tickers['SYMBOL'].eq(symbol).any()) :
      st.write("Invalid Symbol please  refresh the page then enter correct symbol !")
      exit()


  driver(symbol)
  st.write("DB Operations in progress.....")
  t1.join()
  end = time.time()
  log = App_Logger()
  log.log(f"Total Execution time of project : {end - start}")
  st.write("Total Exceution Time : ", end - start)
