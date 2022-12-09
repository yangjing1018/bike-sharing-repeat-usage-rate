import numpy as np
import pandas as pd
import geohash
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def getGeo(x,y):
    return geohash.encode(y,x,precision=7)

if __name__ == "__main__":
    #Generating the variables
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    dic_micro = {"hour":[],"user_unlock":[],"followup_orders_unlock_24h":[],"followup_orders_unlock_24to72r":[],
                  "followup_orders_unlock_72to168h":[],"user_lock":[],"followup_orders_lock_24h":[],
                  "followup_orders_lock_24to72h":[],"followup_orders_lock_72to168h":[],
                   "mean_temp":[],"air":[],"GDP":[]}

    df_macro = pd.read_excel("/Users/yangjing/Desktop/dissertation/macro data.xlsx")
    df_macro.columns = ['date','is_weekday','max_temp','min_temp','mean_temp','is_rain',
                       'air','wind','house_price','population','GDP']
    # df_macro = df_macro[['max_temp','min_temp','air','wind','house_price','population','GDP']]

    for day in range(22,29):
        for i in range(0,24):
            lock_average = len(df[(df["end_time"] >= datetime(2016, 8, day-7,i,0,0)) & (df["end_time"] < datetime(2016, 8, day,i,0,0))])/7
            lock_1 = len(df[(df["end_time"] >= datetime(2016, 8, day-1,i,0,0)) & (df["end_time"] < datetime(2016, 8, day,i,0,0))])
            lock_3 = len(df[(df["end_time"] >= datetime(2016, 8, day-3,i,0,0)) & (df["end_time"] < datetime(2016, 8, day,i,0,0))])
            lock_7 = len(df[(df["end_time"] >= datetime(2016, 8, day-7,i,0,0)) & (df["end_time"] < datetime(2016, 8, day,i,0,0))])

            unlock_average = len(df[(df["start_time"] >= datetime(2016, 8, day-7,i,0,0)) & (df["start_time"] < datetime(2016, 8, day,i,0,0))])/7
            unlock_1 = len(df[(df["start_time"] >= datetime(2016, 8, day-1,i,0,0)) & (df["start_time"] < datetime(2016, 8, day,i,0,0))])
            unlock_3 = len(df[(df["start_time"] >= datetime(2016, 8, day-3,i,0,0)) & (df["start_time"] < datetime(2016, 8, day,i,0,0))])
            unlock_7 = len(df[(df["start_time"] >= datetime(2016, 8, day-7,i,0,0)) & (df["start_time"] < datetime(2016, 8, day,i,0,0))])

            dic_micro["hour"].append(i)
            dic_micro["user_unlock"].append(unlock_average)
            dic_micro["followup_orders_unlock_24h"].append(unlock_1)
            dic_micro["followup_orders_unlock_24to72r"].append(unlock_3)
            dic_micro["followup_orders_unlock_72to168h"].append(unlock_7)
            dic_micro["user_lock"].append(lock_average)
            dic_micro["followup_orders_lock_24h"].append(lock_1)
            dic_micro["followup_orders_lock_24to72h"].append(lock_3)
            dic_micro["followup_orders_lock_72to168h"].append(lock_7)
            dic_micro["mean_temp"].append(df_macro["mean_temp"][0])
            dic_micro["air"].append(df_macro["air"][0])
            dic_micro["GDP"].append(df_macro["GDP"][0])
    x = pd.DataFrame(dic_mirco)

    #Generate repeat usage rate
    df_zi = pd.read_csv("result_repeat usage rate.csv",encoding="gb18030")
    y = pd.DataFrame()
    for day in range(22,29):
        df_day = df_zi[df_zi["date"]==day]
        df_day = df_day.groupby('hour').mean()
        y = pd.concat([y,df_day["48h"]])
    y = y.reset_index(drop=True)
    import statsmodels.api as sm
    print("---------------------------------display the variable---------------------------------\n")
    print(x)
    print("\n"*3)
    print("---------------------------------display the repeat usage rate---------------------------------\n")
    print(y)
    model = sm.OLS(y, x.astype(float))  # generate model
    result = model.fit()  # fit model
    print("\n"*3)
    print("---------------------------------Summary of linear model parameters---------------------------------\n")
    print(result.summary())
    formula = ""
    for o in range(12):
        parameter = str(result.params[o])
        if result.params[o] > 0:
            formula = formula + "+" + parameter + " * " + x.columns[o]
        if result.params[o] < 0:
            formula = formula + parameter + " * " + x.columns[o]
    print("\n"*3)
    print("---------------------------------repeat usage rate---------------------------------\n")
    print("repeat usage rate=",formula)
  
    print("---------------------------------display of evaluation indicators---------------------------------\n")
    yp = result.predict(x)
    resid = y-yp
    rss = np.sum(resid**2)
    MSE = rss/(result.nobs)
    RMSE = np.sum(MSE**2)
    print("RMSE:",RMSE)
    APE = 0
    y = y.values
    for q in range(len(y)):
        APE = abs((yp[q]-y[q])/y[q])
    MAPE = APE / (result.nobs)
    print("MAPE:",MAPE[0])
