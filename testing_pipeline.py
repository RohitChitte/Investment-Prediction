import pandas as pd
from keras.models import load_model
from pickle import load
import matplotlib.pyplot as plt
import numpy as np
import os

from Logger.logging import App_Logger
log_obj = App_Logger()

def testing_data(path):
    try:
        log_obj.log("Entered try block of testing_data function")
        data = pd.read_csv(path)
        new_data = data[["Date","Price"]]
        # print(len(new_data))


        # scaling
        scaler = load(open(r"scaler.pkl",'rb'))


        # scaler = MinMaxScaler(feature_range=(0,1))
        data_testing_array = scaler.fit_transform(new_data[["Price"]])
        log_obj.log("Reading data, loading scaler pickle file and scaling done")
        # print(data_testing_array)

        # splitting x_traing and y_train
        arr = []
        if(data_testing_array.shape[0]>100):
            for i in range(100, data_testing_array.shape[0]):
                arr.append(data_testing_array[i - 100:i])
            log_obj.log("Transformed array returned successfully")
            return np.array(arr)
        else:
            log_obj.log("Size of data is too less to do predictions")
            return "Data Underflow (i.e size of data must be greater than 100"

    except Exception as e:
        log_obj.log(f"Exception occured in testing_data function as follows : {e}")
        # print(e)
        return e




def prediction(data):
    try:
        log_obj.log("entered try block of prediction function")
        model = load_model('New_Model.h5')
        scaler = load(open(r"scaler.pkl",'rb'))
        log_obj.log("Model file and scaler file loaded succesfully")
        # # scaler = MinMaxScaler(feature_range=(0, 1))
        prediction_array = model.predict(data)
        scale_factor = 1/scaler.scale_[0]
        predicted_prices = prediction_array * scale_factor
        log_obj.log("returned predicted prices succesfully exiting prediction function")
        return predicted_prices
    except Exception as e:
        log_obj.log(f"Unexpected Error in prediction function as follows : {e}")
        return e




#
if __name__ == "__main":
    file_name = "Archieve_Files/Nifty-50_Data_from_2000-01-01_to_2023-01-18.csv"
    testing = (testing_data(file_name))

    pred = prediction(testing)
    acutual = pd.read_csv(file_name)[["Price","Date"]][100:]
    # print(testing)
    acutual["Prediction"] = pred



    # print(len(pred),len(acutual))
    plt.figure(figsize=(12,6))
    # plt.plot_date(acutual["Date"], acutual["Price"], 'b',label="Actual Price")
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.gca().xaxis.set_tick_params(rotation = 90, labelsize=3)
    plt.plot(acutual["Price"],'b',label = 'Actual Price')
    plt.plot(acutual["Prediction"], 'r', label = 'Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    # plt.show()
    file_name = "test"

    (os.chdir(os.getcwd()[:63]))
    path = (os.getcwd()[:63] + "\\" + f"Archieve_Files\\Prediction Figures\{os.listdir('Data/Scraped Data')[0]}"[:-4]+".png")
    plt.savefig(path)
    print("rohit")

#
