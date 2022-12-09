import pandas as pd
import geohash
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


def getGeo(x,y):
    return geohash.encode(y,x,precision=7)

if __name__ == "__main__":
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    dic_micro = {"user_unlock":[],"followup_orders_unlock_24h":[],"followup_orders_unlock_24to72r":[],
                  "followup_orders_unlock_72to168h":[],"user_lock":[],"followup_orders_lock_24h":[],
                  "followup_orders_lock_24to72h":[],"followup_orders_lock_72to168h":[]}

    df_macro = pd.read_excel("/Users/yangjing/Desktop/dissertation/macto data22_31.xlsx")
    df_macro.columns = ['date','is_weekday','max_temp','min_temp','mean_temp','is_rain',
                       'air','wind','house_price','population','GDP']
    df_macro = df_macro[['max_temp','min_temp','air','wind','house_price','population','GDP']]

    for i in range(22,29):
        lock_average = len(df[(df["end_time"] >= datetime(2016, 8, i-7)) & (df["start_time"] < datetime(2016, 8, i,0,0,0))])/7
        lock_1 = len(df[(df["start_time"] >= datetime(2016, 8, i - 1)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])
        lock_3 = len(df[(df["start_time"] >= datetime(2016, 8, i - 3)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])
        lock_7 = len(df[(df["start_time"] >= datetime(2016, 8, i - 7)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])

        unlock_average = len(df[(df["end_time"] >= datetime(2016, 8, i-7)) & (df["start_time"] < datetime(2016, 8, i,0,0,0))])/7
        unlock_1 = len(df[(df["end_time"] >= datetime(2016, 8, i - 1)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])
        unlock_3 = len(df[(df["end_time"] >= datetime(2016, 8, i - 3)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])
        unlock_7 = len(df[(df["end_time"] >= datetime(2016, 8, i - 7)) & (df["start_time"] < datetime(2016, 8, i, 0, 0, 0))])

        dic_micro["user_unlock"].append(unlock_average)
        dic_micro["followup_orders_unlock_24h"].append(unlock_1)
        dic_micro["followup_orders_unlock_24to72r"].append(unlock_3)
        dic_micro["followup_orders_unlock_72to168h"].append(unlock_7)
        dic_micro["user_lock"].append(lock_average)
        dic_micro["followup_orders_lock_24h"].append(lock_1)
        dic_micro["followup_orders_lock_24to72h"].append(lock_3)
        dic_micro["followup_orders_lock_72to168h"].append(lock_7)
    df_micro = pd.DataFrame(dic_micro)

    df_all = pd.concat([df_micro,df_macro],axis=1)
    df_all.astype(float)

    # plt.subplots(figsize=(20, 15))
    plt.subplots()
    ax = plt.axes()
    ax.set_title("Correlation Heatmap")
    corr = df_all.corr()

    sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values)
    plt.tight_layout()
    plt.savefig("/Users/yangjing/Desktop/dissertation/pearson", dpi=600)
    plt.show()
    df_all.to_csv("data_table2_table3.csv", index=False, sep=',', encoding="gb18030")
    corr.to_csv("result_pearson.csv", index=False, sep=',', encoding="gb18030")
