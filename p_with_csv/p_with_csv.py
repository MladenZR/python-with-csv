import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import normal


#import data from tables 
dfsp = pd.read_csv("SP500.csv")
dfb = pd.read_csv("BTC.csv")

#rename column name
df1 = dfb.rename(index=str, columns={"Adj Close": "AdjCloseBTC"})
df2 = dfsp.rename(index=str, columns={"Adj Close": "AdjCloseSP500"})

#standardize data as daily pct return
df1['BTCpct'] =  (df1['AdjCloseBTC'] - df1['AdjCloseBTC'].shift(+1))/df1['AdjCloseBTC'].shift(+1)*100
df2['SP500pct'] =  (df2['AdjCloseSP500'] - df2['AdjCloseSP500'].shift(+1))/df2['AdjCloseSP500'].shift(+1)*100

#concatt target columns from two differente table
df3 = pd.concat([df1['Date'],df1['BTCpct']],axis=1)
df4 = pd.concat([df2['Date'],df2['SP500pct']],axis=1)

#merge columns by date and drop whole row if value in any cell are NaN
df5 = df3.merge(df4, how='left', on='Date').dropna()

#drop complete row if value in any cell greater than 3
df6=df5[df5['BTCpct']  < 3].copy()

#df6['pct'] = np.where((df6['BTCpct'] >=0.5) & (df6['BTCpct']<=1), "0.05", "0")
#dfsp["-0.05pct"] = np.where((df['pct'] >=-0.05) & (df['pct'] <=0), '1', '0')

#value distribution BTCptc
def groupBTCpct(BTCpct):
    if  (BTCpct >0 and BTCpct<=0.5):
        return "0.5"
    elif (BTCpct >0.5 and BTCpct<=1):
        return "1"
    elif (BTCpct >1 and BTCpct<=1.5):
        return "1"
    elif (BTCpct >1.5 and BTCpct<=2):
        return "1.5"
    elif (BTCpct >2 and BTCpct<=2.5):
        return "2"
    elif (BTCpct >2.5 and BTCpct<=3):
        return "2.5"
    elif  (BTCpct >-0.5 and BTCpct<0):
        return "-0.5"
    elif  (BTCpct >-1 and BTCpct<-0.5):
        return "-1"
    elif  (BTCpct >-1.5 and BTCpct<-1):
        return "-1.5"
    elif  (BTCpct >-2 and BTCpct<-1.5):
        return "-2"
    elif  (BTCpct >-2.5 and BTCpct<-2):
        return "-2.5"
    elif  (BTCpct >-3 and BTCpct<-2.5):
        return "-3"
    else:
        return "0"
df6['BTCpct_group']= df6.BTCpct.apply(groupBTCpct)

#value distribution SP500pct
def groupSP500pct(SP500pct):
    if  (SP500pct >=0):
        return "1"
    elif (SP500pct <0):
        return "-1"
    else:
        return "0"
df6['SP500pct_group'] = df6.SP500pct.apply(groupSP500pct)


#pivot table SP500pct_group / BTCpct_group
func = lambda x: 100*x.count()/df6.shape[0]
df7 =pd.pivot_table(df6, columns=["SP500pct_group"], index=["BTCpct_group"], aggfunc={"SP500pct_group":func})

df8=df7.SP500pct_group

def groupBTCpct(BTCpct):
    if  (BTCpct_group >0 and BTCpct_group<=0.5 and SP500pct_group >=0):
        return "1"
    else:
        return "0"
#10-day moving average BTCpct_group column    
df6["MA_BTCpct_group"] = df6['BTCpct_group'].rolling(window=10).mean()


# Histogram
hist = df6.hist(bins=20)
plt.show()

#descriptive statistics
df7=(df6).describe()
print(df6)
print(df7)
print(df8)
