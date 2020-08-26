import requests
import datetime
import sklearn
from sklearn.preprocessing import MinMaxScaler
import math
import numpy as np
import pandas as pd
import joblib

apiKey = 'a4cc8e69c6804cfb8c8e69c680ccfb10' 
stationId =  'ICTPUERT3' # ALUAR:['ICHUBUTP5','ICHUBUTP4'],  Local : 'ICTPUERT3'
yesterday = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1),"%Y%m%d")

def request_last_24hs():
    df_list = []
    number = 0
    try: 
        response = requests.get(
        f'https://api.weather.com/v2/pws/history/hourly?stationId={stationId}&format=json&units=m&date={yesterday}&apiKey={apiKey}', 
        headers={'Accept': 'application/json'})
        data = response.json()
        
        number += 1
        for i in data['observations']:
            new_dict = {k: v for k, v in i.items() if k != 'metric'}
            aa = pd.DataFrame(new_dict,index=[new_dict['obsTimeLocal']])
            bb = pd.DataFrame(i['metric'],index=[new_dict['obsTimeLocal']]) 
            cc = aa.merge(bb,left_index=True, right_index=True)
            # select certain columns
            #df = cc[['solarRadiationHigh','winddirAvg','humidityAvg','tempAvg','windspeedAvg','dewptAvg','pressureMax', 'precipTotal']]
        
            # each set of measurements is append to a list, we will convert it into a pandas dataframe at the end
            df_list.append(cc)
            df = pd.concat(df_list)[['solarRadiationHigh','humidityAvg','tempAvg', 'windspeedAvg',
                                     'dewptAvg', 'pressureMax','precipTotal']]
    except:
        pass
    return df

#df = request_last_24hs()

def preprocess(df):
    df_predict = pd.DataFrame(columns=['solar_Avg', 'windspeed_Avg', 'precip_Avg', 'month', 'dew_Avg',
       'temp_Avg', 'humid_Avg', 'temp_min', 'temp_max', 'solar_max', 'dew_min',
       'humid_min', 'humid_max', 'dew_max', 'pressure_std', 'temp_23',
       'temp_diff', 'temp_max_diff', 'temp_min_diff', 'temp_maxAvg_weekly',
       'temp_minAvg_weekly'])
    df = df.astype('float32')
    df.index = pd.to_datetime(df.index)
    
    df_predict = df_predict.append({'solar_Avg':df['solarRadiationHigh'].median()}, ignore_index=True)
    
    df_predict['windspeed_Avg'] = df['windspeedAvg'].median()
    
    df_predict['precip_Avg'] = df['precipTotal'].median()
    
    df_predict['month'] = math.cos( ((df.index[0].month - 1)/11) * 2 * 3.14159265)
    
    df_predict['dew_Avg'] = df['dewptAvg'].median()
    
    df_predict['temp_Avg'] = df['tempAvg'].median()
    
    df_predict['humid_Avg'] = df['humidityAvg'].median()
    
    df_predict['temp_min'] = df['tempAvg'].min()
    
    df_predict['temp_max'] = df['tempAvg'].max()
    
    df_predict['solar_max'] = df['solarRadiationHigh'].max()
    
    df_predict['dew_min'] = df['dewptAvg'].min()
    
    df_predict['humid_min'] = df['humidityAvg'].min()
    
    df_predict['humid_max'] = df['humidityAvg'].max()
    
    df_predict['dew_max'] = df['dewptAvg'].max()
    
    df_predict['pressure_std'] = df['pressureMax'].std()
    
    df_predict['temp_23'] = df['tempAvg'][-1]
    
    df_predict['temp_diff'] = df['tempAvg'].max() - df['tempAvg'].min()
    
    #to improve later:
    df_predict['temp_max_diff'] = 0.
    df_predict['temp_min_diff'] = 0.
    df_predict['temp_maxAvg_weekly'] = 16.
    df_predict['temp_minAvg_weekly'] = 6.
    
    # normalization
    scaler = joblib.load('scaler.pkl')
    to_predict = scaler.transform(df_predict)

    #prediction
    model = joblib.load('model_min.pkl')
    min_temp = model.predict(to_predict)

    return min_temp


def request_preproc():
    df = request_last_24hs()
    min_temp = preprocess(df)
    min_temp = int(float(min_temp))
    return str(min_temp)
        
            