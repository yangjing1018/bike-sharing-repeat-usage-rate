section 3.1 figures.py

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from datetime import datetime
sns.set_palette("Set2")
pd.options.mode.chained_assignment = None

def line_morning_peak(df):
    x_date,y_orderNum = [],[]
    for i in range(1,32):
        lock_average = df[(df["start_time"] >= datetime(2016, 8, i,7,0,0)) & (df["end_time"] < datetime(2016, 8, i,9,0,0))]
        x_date.append(i)
        y_orderNum.append(len(lock_average))
    plt.plot(x_date, y_orderNum, 'ro-', color='#4169E1', alpha=0.8, linewidth=1)
    # plt.legend(loc="upper right"), label='some numbers'
    plt.xlabel('date')
    plt.ylabel('orderNumber')
    plt.savefig("/Users/yangjing/Desktop/dissertation/Daily morning peak 7-9 order total line graph.png",dpi=600)
    plt.show()

def line_night_peak(df):
    x_date,y_orderNum = [],[]
    for i in range(1,32):
        lock_average = df[(df["start_time"] >= datetime(2016, 8, i,17,0,0)) & (df["end_time"] < datetime(2016, 8, i,19,0,0))]
        x_date.append(i)
        y_orderNum.append(len(lock_average))
    plt.plot(x_date, y_orderNum, 'ro-', color='#4169E1', alpha=0.8, linewidth=1)
    # plt.legend(loc="upper right"), label='some numbers'
    plt.title('daily morning peak data for August')
    plt.xlabel('date')
    plt.ylabel('orderNumber')
    plt.savefig("/Users/yangjing/Desktop/dissertation/Daily evening peak 17-19 order total line graph.png", dpi=600)
    plt.show()

def histogram_week(df):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 20))
    y_1,y_2,y_3,y_4 = [],[],[],[]
    for i in range(1,8):
        df_day = df[(df["start_time"] >= datetime(2016, 8, i, 7, 0, 0)) & (df["end_time"] < datetime(2016, 8, i, 9, 0, 0))]
        y_1.append(len(df_day))
        df_day = df[(df["start_time"] >= datetime(2016, 8, i+7, 7, 0, 0)) & (df["end_time"] < datetime(2016, 8, i+7, 9, 0, 0))]
        y_2.append(len(df_day))
        df_day = df[(df["start_time"] >= datetime(2016, 8, i+14, 7, 0, 0)) & (df["end_time"] < datetime(2016, 8, i+14, 9, 0, 0))]
        y_3.append(len(df_day))
        df_day = df[(df["start_time"] >= datetime(2016, 8, i+21, 7, 0, 0)) & (df["end_time"] < datetime(2016, 8, i+21, 9, 0, 0))]
        y_4.append(len(df_day))
    x = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    x_color = ["green","green","green","green","green","red","red"]
    axes[0][0].bar(x, y_1, 0.7, color=x_color)
    axes[0][0].set_title ("8.1-8.7",size=30)
    axes[0][1].bar(x, y_2, 0.7, color=x_color)
    axes[0][1].set_title ("8.7-8.14",size=30)
    axes[1][0].bar(x, y_3, 0.7, color=x_color)
    axes[1][0].set_title ("8.15-8.21",size=30)
    axes[1][1].bar(x, y_4, 0.7, color=x_color)
    axes[1][1].set_title ("8.22-8.28",size=30)
    plt.savefig("/Users/yangjing/Desktop/dissertation/Line graph of the total number of orders per day for four weeks.png", dpi=600)
    plt.show()

def line_exeryhour(df):
    fig, axes = plt.subplots(nrows=4, ncols=5, figsize=(20, 20))
    Y = []
    for i in range(1,29):
        if i not in [6,7,13,14,20,21,27,28]:
            y = []
            for h in range(24):
                if h != 23:
                    df_hour = df[(df["start_time"] >= datetime(2016, 8, i, h, 0, 0)) & (df["end_time"] < datetime(2016, 8, i, h+1, 0, 0))]
                else:
                    df_hour = df[(df["start_time"] >= datetime(2016, 8, i, h, 0, 0)) & (df["end_time"] < datetime(2016, 8, i+1, 0, 0, 0))]
                y.append(len(df_hour))
        Y.append(y)
    for p in range(20):
        axes[p//5][p%5].plot([_ for _ in range(1,25)],Y[p],'ro-', color='#4169E1', alpha=0.8, linewidth=1)
        # ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if p%5 ==0:
            axes[p // 5][p % 5].set_title("Monday")
        if p%5 ==1:
            axes[p // 5][p % 5].set_title("Tuesday")
        if p%5 ==2:
            axes[p // 5][p % 5].set_title("Wednesday")
        if p%5 ==3:
            axes[p // 5][p % 5].set_title("Thursday")
        if p%5 ==4:
            axes[p // 5][p % 5].set_title("Friday")
    plt.savefig("/Users/yangjing/Desktop/dissertation/Line graph of the total number of orders per hour on a working day.png", dpi=600)
    plt.show()

if __name__ == "__main__":
    # Morning peak, evening peak box line map Network map
    # Change in order volume in a day Line chart Pick 7 days 
    # Individual bicycle usage during the week Bar graphs Network graphs
    # ['orderid', 'bikeid', 'userid', 'start_time', 'start_location_x','start_location_y',
    #  'end_time', 'end_location_x', 'end_location_y', 'track']
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    dic_micro = {"user_unlock":[],"followup_orders_unlock_24h":[],"followup_orders_unlock_24to72r":[],
                  "followup_orders_unlock_72to168h":[],"user_lock":[],"followup_orders_lock_24h":[],
                  "followup_orders_lock_24to72h":[],"followup_orders_lock_72to168h":[]}

    df_macro = pd.read_excel("/Users/yangjing/Desktop/dissertation/macro data.xlsx")
    df_macro.columns = ['date','is_weekday','max_temp','min_temp','mean_temp','is_rain',
                       'air','wind','house_price','population','GDP']
    df_macro = df_macro[['max_temp','min_temp','air','wind','house_price','population','GDP']]
    print(df.columns)
    # sns.boxplot(y="bikeid",data=df)

    #Create a line graph to show the morning and evening peaks
    # line_morning_peak(df)
    # line_night_peak(df)

    # 发There are now four lows in both the morning and evening peaks, 
    # so four full weeks from 8.1 - 8.28 were selected for the bar chart presentation to analyse the fluctuations
    # histogram_week(df)


    #Line chart Statistics on usage by hour of the day Selected weekdays
    # line_exeryhour(df)
    #Keeping statistics on bicycle usage
    bike = set(df["bikeid"].tolist())
    print(bike)
    print(len(bike))
    # plt.show()