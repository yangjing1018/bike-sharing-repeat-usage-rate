#calculation of the repeat usage rate.py


import pandas as pd
import geohash
from datetime import datetime
from collections import Counter


def getGeo(x,y):
    return geohash.encode(y,x,precision=4)

if __name__ == "__main__":
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated_new.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    #1\get date from 22 to 31
    df = df[df["start_time"] >= datetime(2016, 8, 22)]
    df = df[df["start_time"] <= datetime(2016, 8, 31)]

    #Calculating the geohash area at the start and end 2016.8.24 17:00-18:00
    df["start_geo"] = df.apply(lambda x: getGeo(x["start_location_x"],x["start_location_y"]), axis=1)
    df["end_geo"] = df.apply(lambda x: getGeo(x["end_location_x"], x["end_location_y"]), axis=1)
    # print(set(df["start_location_geo"].tolist()))
    # print(len(set(df["start_location_geo"].tolist())))
    # df10 = df[df["start_location_geo"]=="wtq"]
    # df11 = df[df["start_location_geo"] == "wtw"]
    # print(df10["start_location_x"].mean(), df10["start_location_y"].mean())
    # print(df10["end_location_x"].mean(), df10["end_location_y"].mean())
    # exit()
    # df_no_samegeo = df[df["start_location_geo"] != df["end_location_geo"]]  #
    # print(df_no_samegeo)
    #Calculate the 24-hour and 48-hour repeat usage rates for each time period and region from 25 August to 29 August to generate
    #result_repeat usage rate.csv
    dict_repeat usage rate = {"date":[],"hour":[],"region":[],"24h":[],"48h":[]}
    for day in range(22,29):#Traversing each day
        for hour in range(0,24):#Traversing each hour
            #24 and 48 hours after the current hour
            if hour != 23:
                df_bike = df[df["start_time"] >= datetime(2016, 8, day, hour + 1, 0, 0)]
                df_bike_24 = df_bike[df_bike["end_time"] <= datetime(2016, 8, day + 1, hour + 1, 0, 0)]
                df_bike_48 = df_bike[df_bike["end_time"] <= datetime(2016, 8, day + 2, hour + 1, 0, 0)]
            else:
                df_bike = df[df["start_time"] >= datetime(2016, 8, day + 1, 0, 0, 0)]
                df_bike_24 = df_bike[df_bike["end_time"] <= datetime(2016, 8, day + 2, 0, 0, 0)]
                df_bike_48 = df_bike[df_bike["end_time"] <= datetime(2016, 8, day + 3, 0, 0, 0)]

            print("start calculate August", day,"day，",hour,"h")

            #Get orders for the current time period
            df_target = df[df["start_time"] >= datetime(2016, 8, day,hour,0,0)]
            if hour != 23:
                df_target = df_target[df_target["end_time"] >= datetime(2016, 8, day, hour+1, 0, 0)]
            else:
                df_target = df_target[df_target["end_time"] >= datetime(2016, 8, day+1, 0, 0, 0)]
            #Get all the regions with orders in that time period, de-duplicate and compose a list
            list_geo = list(set(df_target["start_geo"].to_list()))
            print("overall ",len(list_geo),"regions")

            #After a fixed period of time, start traversing each area,calculate the repeat usage rate
            for geo in list_geo:
                df_geo = df_target[df_target["start_geo"]==geo]
                list_bike = list(set(df_geo["bikeid_geo"].to_list()))
                num_24,num_48 = 0,0
                print("allover have", len(list_bike), "bikes")
                for bike in list_bike:
                    num_bike_ed_24 = len(df_bike_24[df_bike_24["bikeid_geo"]==bike])
                    num_bike_ed_48 = len(df_bike_48[df_bike_48["bikeid_geo"] == bike])
                    # print(num_bike_ed_24,num_bike_ed_48)
                    num_24 += num_bike_ed_24
                    num_48 += num_bike_ed_48
                result_24 = (num_24 - len(list_bike))/len(list_bike)
                result_48 = (num_48 - len(list_bike)) / len(list_bike)
                # {"date": [], "hour": [], "region": [], "24h": [], "48h": []}
                dict_repeat usage rate["date"].append(day)
                dict_repeat usage rate["hour"].append(hour)
                dict_repeat usage rate["region"].append(geo)
                dict_repeat usage rate["24h"].append(result_24)
                dict_repeat usage rate["48h"].append(result_48)
    dataframe_csv = pd.DataFrame(dict_repeat usage rate)
    dataframe_csv.to_csv("result_repeat usage rate.csv", index=False, sep=',', encoding="gb18030")
