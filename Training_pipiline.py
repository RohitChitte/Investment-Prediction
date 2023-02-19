import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
from datetime import datetime
import pytz
from pickle import load, dump


def training_data(path):
    try:

        data = pd.read_csv(path)
        new_data = data

        # Splitting data
        data_training = pd.DataFrame(new_data['Price'][0:int(len(new_data) * 0.70)])
        data_testing = pd.DataFrame(new_data['Price'][int(len(new_data) * 0.70):int(len(new_data))])
        print(training_data)
        # scaling
        scaler = MinMaxScaler(feature_range=(0, 1))
        data_training_array = scaler.fit_transform(data_training)

        # splitting x_traing and y_train
        x_train = []
        y_train = []

        for i in range(100, data_training_array.shape[0]):
            x_train.append(data_training_array[i - 100:i])
            y_train.append(data_training_array[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        dump(scaler, open("scaler.pkl", 'wb'))
        return x_train, y_train
    except Exception as e:
        return e


def model_training(x_train, y_train):
    model = Sequential()
    model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=60, activation='relu', return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(units=80, activation='relu', return_sequences=True))
    model.add(Dropout(0.4))

    model.add(LSTM(units=120, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=50)

    IST = pytz.timezone('Asia/Kolkata')

    model_file_name = (f"Model_File_{str(datetime.now(IST))[0:10]}_{str(datetime.now(IST))[11:16]}")

    model.save(model_file_name)
    return model


#x_train, y_train = training_data(r"/content/Nifty-50_Data_from_2000-01-01_to_2023-01-18.csv")
#model = model_training(x_train, y_train)
