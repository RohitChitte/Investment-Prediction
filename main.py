import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import Data_Scrapping
import  testing_pipeline
import DB_Files.Cassandra_Database
import threading
from Logger.logging import App_Logger
import streamlit as st

def driver():

    symbol = input("Enter stock Ticker : ").upper()
    tickers = pd.read_csv(r"Data/Static Data/EQUITY.csv")

    while not (tickers['SYMBOL'].eq(symbol)).any():
        symbol = input("Enter valid Stock Ticker : ")


    data = Data_Scrapping.scrap_data_from_yahoo_finance(symbol)

    t1.start()

    filename = os.listdir("Data\Scraped Data")[0]
    testing = testing_pipeline.testing_data(f"Data\Scraped Data\{filename}")

    pred = testing_pipeline.prediction(testing)
    actual_vs_predicted = pd.read_csv("Data\Scraped Data\\"+filename)[["Price","Date"]][100:]
    # print(testing)
    actual_vs_predicted["Prediction"] = pred


    plt.figure(figsize=(12,6))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.plot(actual_vs_predicted["Price"],'b',label = 'Actual Price')
    plt.plot(actual_vs_predicted["Prediction"], 'r', label = 'Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    # plt.show()
    # Saving png file to archieve/Prediction Figures
    (os.chdir(os.getcwd()[:63]))
    path = (os.getcwd()[:63] + "\\" + f"Archieve_Files\\Prediction Figures\{os.listdir('Data/Scraped Data')[0]}"[:-4]+".png")
    if (os.path.exists(path)):
        os.remove(path)
    plt.savefig(path)



def Db():
    DB_obj = DB_Files.Cassandra_Database.CassandraDBManagement()
    DB_obj.upload_data_to_DB('demo')
    print(DB_obj.fetch_data_from_table_in_DB('demo'))



start = time.time()
t1 = threading.Thread(target=Db)
driver()
print("DB operations in progress .......")
t1.join()
end = time.time()
log = App_Logger()
log.log(f"Total Execution time of project : {end-start}")
print("Total Exceution Time : ",end-start)