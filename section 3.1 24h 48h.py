import csv

import pandas as pd


if __name__ == "__main__":
    f = open("result_repeat usage rateDescribe.csv", "a", newline="")
    w = csv.writer(f)
    w.writerow(["", "24h", "48h"])
    df = pd.read_csv("result_repeat usage rate.csv",encoding="gb18030")
    w.writerow(["mean",df.mean()[2],df.mean()[3]])
    w.writerow(["standard deviation", df.std()[2], df.std()[3]])
    w.writerow(["median", df.median()[2], df.median()[3]])
    w.writerow(["skewness", df.skew()[2], df.skew()[3]])
    w.writerow(["kurtosis ", df.kurt()[2], df.kurt()[3]])

