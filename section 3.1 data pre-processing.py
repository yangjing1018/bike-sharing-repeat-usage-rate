#section 3.1 data pre-processing.py


import pandas as pd
import geohash
from datetime import datetime
from collections import Counter


def getGeo(x,y):
    return geohash.encode(y,x,precision=6)#6-1715  5-114 4-11

def getBike_geo(id,dic_bike_geo4):
    return dic_bike_geo4[id]

if __name__ == "__main__":
    df = pd.read_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated.csv")
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    #1\Get data for 25 to 31
    # df = df[df["start_time"] >= datetime(2016, 8, 25)]
    # df = df[df["start_time"] <= datetime(2016, 8, 31)]

    #Calculating the geohash area at the start end 2016.8.24 17:00-18:00
    df["start_location_geo"] = df.apply(lambda x: getGeo(x["start_location_x"],x["start_location_y"]), axis=1)
    df["end_location_geo"] = df.apply(lambda x: getGeo(x["end_location_x"], x["end_location_y"]), axis=1)

    dic_bike_geo4 = {}
    bikes = df["bikeid"].tolist()
    for i_b in range(len(bikes)):
        bike = bikes[i_b]
        if bike not in dic_bike_geo4:
            dic_bike_geo4[bike] = df["start_location_geo"][i_b]
    df["bikeid_geo"] = df["bikeid"].apply(getBike_geo,dic_bike_geo4=dic_bike_geo4)
    df.to_csv("/Users/yangjing/Desktop/dissertation/mobike_shanghai_sample_updated_new.csv", index=False, sep=',', encoding="gb18030")


    