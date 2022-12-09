import pandas as pd
import geohash
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_boston

def regularit(df):
    newDataFrame = pd.DataFrame(index=df.index)
    columns = df.columns.tolist()
    for c in columns:
        d = df[c]
        MAX = d.max()
        MIN = d.min()
        newDataFrame[c] = ((d - MIN) / (MAX - MIN)).tolist()
    return newDataFrame


def getGeo(x,y):
    return geohash.encode(y,x,precision=7)

if __name__ == "__main__":
    #generate variables
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    dic_micro = {"hour":[],"user_unlock":[],"followup_orders_unlock_24h":[],"followup_orders_unlock_24to72r":[],
                  "followup_orders_unlock_72to168h":[],"user_lock":[],"followup_orders_lock_24h":[],
                  "followup_orders_lock_24to72h":[],"followup_orders_lock_72to168h":[],
                   "mean_temp":[],"air":[],"GDP":[]}

    df_macro = pd.read_excel("/Users/yangjing/Desktop/dissertation/macro.xlsx")
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
    x = pd.DataFrame(dic_micro)#complete variables

    #generate repeat usage rate
    df_zi = pd.read_csv("result_repeat usage rate.csv",encoding="gb18030")
    y = pd.DataFrame()
    for day in range(22,29):
        df_day = df_zi[df_zi["date"]==day]
        df_day = df_day.groupby('hour').mean()
        y = pd.concat([y,df_day["48h"]])
    y = y.reset_index(drop=True)

    print("---------------------------------display variables---------------------------------\n")
    name = x.columns
    x = x.astype(float)
    print("\n"*3)
    print("---------------------------------display variables---------------------------------\n")
    y = y.values
    y = y.astype(np.float)
    print(y)
    print("\n"*3)
    print("---------------------------------Summary of XGBoost parameters---------------------------------\n")
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=15)
    from xgboost import XGBRegressor
    xgb = XGBRegressor(n_estimators=500,
                       max_depth=5,
                       learning_rate=0.1,
                       gamma=0,
                       min_child_weight=1,
                       reg_alpha=0,
                       reg_lambda=1
                       )
    xgb.fit(X_train, y_train)
    print(xgb.feature_importances_)
    plt.barh(name, xgb.feature_importances_)
    plt.tight_layout()
    plt.savefig("/Users/yangjing/Desktop/dissertation/XGBoost", dpi=600)
    plt.show()
    print("---------------------------------display of evaluation indicators---------------------------------\n")
    from sklearn.metrics import mean_squared_error,r2_score
    y_pred = xgb.predict(X_test)
    RMSE = np.sqrt(mean_squared_error(y_pred, y_test))

    APE = []
    for t in range(len(y_test)):
        per_err = (y_test[t] - y_pred[t]) / y_test[t]
        per_err = abs(per_err)
        APE.append(per_err)
    MAPE = sum(APE) / len(APE)
    print("R-squared=",r2_score(y_test,y_pred))
    print("RMSE=", RMSE)
    print("MAPE=", MAPE[0])