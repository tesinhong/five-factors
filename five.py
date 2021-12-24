import pandas as pd
import math
import numpy as np 
import matplotlib.pyplot as plt

import statsmodels.formula.api as sm # module for stats models
from statsmodels.iolib.summary2 import summary_col # module for presenting stats models outputs nicely

# 後でnp.dotの値を上書きするclassを作成
class overwrite:
  test = 0

# predictという変数にoverwriteクラスをインスタンス化
predict = overwrite

# csvファイルにする関数
def pdCsv(fileName):
  fullDir = '/Users/hongtaishen/Desktop/programming/work/vagrant/python/kandai/quant/'
  readFile = fullDir+fileName
  # df_stkをグローバル変数に
  global df_stk
  df_stk = pd.read_csv(readFile,index_col='Date',parse_dates=True)

def price2ret(prices,retType='simple'):
    if retType == 'simple':
        ret = (prices/prices.shift(1))-1
    else:
        ret = np.log(prices/prices.shift(1))
    return ret

def assetPriceReg(df_stk):
    import pandas_datareader.data as web  # module for reading datasets directly from the web
    #from datetime import datetime
    #st = datetime(2021, 10, 1)
    #ed = datetime(2021, 12, 1)
    #df_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench    ', st,ed)[0]

    # Reading in factor data
    df_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench')[0]
    df_factors.rename(columns={'Mkt-RF': 'MKT'}, inplace=True)
    df_factors['MKT'] = df_factors['MKT']/100
    df_factors['SMB'] = df_factors['SMB']/100
    df_factors['HML'] = df_factors['HML']/100
    df_factors['RMW'] = df_factors['RMW']/100
    df_factors['CMA'] = df_factors['CMA']/100
    df_factors['One'] = 1
    print(df_factors)

    df_stock_factor = pd.merge(df_stk,df_factors,left_index=True,right_index=True) 
    # Merging the stock and factor returns dataframes together
    df_stock_factor['XsRet'] = df_stock_factor['Returns'] - df_stock_factor['RF'] # Calculating excess returns

    # Running CAPM, FF3, and FF5 models.
    CAPM = sm.ols(formula = 'XsRet ~ MKT', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF3 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})
    FF5 = sm.ols( formula = 'XsRet ~ MKT + SMB + HML + RMW + CMA', data=df_stock_factor).fit(cov_type='HAC',cov_kwds={'maxlags':1})

    CAPMtstat = CAPM.tvalues
    FF3tstat = FF3.tvalues
    FF5tstat = FF5.tvalues

    CAPMcoeff = CAPM.params
    FF3coeff = FF3.params
    FF5coeff = FF5.params

    # DataFrame with coefficients and t-stats
    results_df = pd.DataFrame({'CAPMcoeff':CAPMcoeff,'CAPMtstat':CAPMtstat,
                               'FF3coeff':FF3coeff, 'FF3tstat':FF3tstat,
                               'FF5coeff':FF5coeff, 'FF5tstat':FF5tstat,
                               'One':1},
    index = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])


    dfoutput = summary_col([CAPM,FF3, FF5],stars=True,float_format='%0.4f',
                  model_names=['CAPM','FF3','FF5'],
                  info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),
                             'Adjusted R2':lambda x: "{:.4f}".format(x.rsquared_adj)},
                             regressor_order = ['Intercept', 'MKT', 'SMB', 'HML', 'RMW', 'CMA'])

    print(dfoutput)

    return results_df



# csvファイルを処理する関数
def calculate(df_stk, predict):
  df_stk.head()
  df_stk.drop(['Volume'],axis=1,inplace=True)
  #df_stk.plot()
  
  df_stk['Returns'] = price2ret(df_stk[['Adj Close']])
  df_stk = df_stk.dropna()
  df_stk.head()
  df_stk['Returns'].plot()
  #print(df_stk['Returns'].hist(bins=20))
  df_regOutput = assetPriceReg(df_stk)
  print(df_regOutput)
 
  #FF3coefと1を入れる空の配列を作成
  array = np.array([])
  one = np.array([])
 
  #np.dot(df_regOutput['FF3coef'], 1が入った配列)をするとnanになるためfor文で計算
  for i in df_regOutput['FF3coeff']:
 
    #iに入ってる値がnanなのかチェック
    if math.isnan(i) == False:
 
      #nanじゃなければそれぞれ値を配列に追加
      array = np.append(array, i)
      one = np.append(one, 1)
    else:
 
      #nanが来た時点でnp.dotで計算をしてfor文を終了
      predict.test = np.dot(array, one)
      break

from pathlib import Path
import sys
import os

home = str(Path.home())

stkName = 'AAPL'
fileName = 'df_price_AAPL_2021-12-17' + '.csv'

# pdCsv関数を呼び出し
pdCsv(fileName)

# 新しい方のアップルのデータを計算
calculate(df_stk, predict)
#print(df_stk['Returns'])
print(predict.test)

#a = np.array([]) # 1+rにpredict,testをかけた値を保存する配列
#b = np.array([]) # 実際のリターンの配列
#for i in df_stk['Returns']:
  #if math.isnan(i) == True:
   # continue
  # ここ間違えてる！！！！！！！！！
  #c = predict.test * i # aに保存する値を算出
  #a = np.append(a, c) # cで出力された値を配列に追加
  #b = np.append(b, i) # iの値を配列に追加

#print(a)
#print(b)

fig, ax = plt.subplots()
t = np.linspace(0, 10, 1000)
#ax.plot(a, color="red", label="predict_return")
#ax.plot(b, color="blue", label="aapl_return")
fig.tight_layout()
#plt.show()

# 古い方のアップルのデータを取得、関数呼び出し
fileName = 'df_price_AAPL_2021-12-17_old_data' + '.csv'
pdCsv(fileName)

# 古い方のアップルのデータを計算
calculate(df_stk, predict)
#print(predict.test)
