import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

def ifweekday(day):
      if day == 25:
            return 0
      if day == 26:
            return 0
      if day == 27:
            return 1
      if day == 28:
            return 1
      if day == 29:
            return 0
# ANOVA

df = pd.read_csv("result_repeat usage rate.csv", encoding="gb18030")
df.columns = ["day", "hour", "area", "value", "repeat usage rate"]
df["weekday"] = df.day.apply(ifweekday)

data_week = df[["weekday", "value"]]
model_week = ols('value ~C(weekday)', data = data_week).fit()
anova_week = anova_lm(model_week, type = 2)
print(anova_week)

data_hour = df[["hour", "value"]]
model_hour = ols('value ~C(hour)', data = data_hour).fit()
anova_hour = anova_lm(model_hour, type = 2)
print(anova_hour)


