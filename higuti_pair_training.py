# ペアトレ発表　平田＆樋口

 

 

 

1. ペアトレに必要なライブラリ？をインポートする。

 

とりあえず　ぺあとれの要領で見つけた2銘柄の価格を図示するとぐにゃぐにゃになるか　を調べるためには

 

①距離の短い2銘柄を探す

②その2銘柄のポートフォリオ(株の枚数比)価値を算出する=2銘柄の価格を表した図を書くには2銘柄を何枚ずつ買うのかを決める必要あってそのポートフォリオで、2銘柄のポートフォリオ価値(株の合計価格がどうなるか見なあかん

③2銘柄のポートフォリオ価値を図示してぐにゃぐにゃになってるか見る

 

import qnt.data as qndata

import numpy as np

import itertools

 

#future_list=qndata.futures.load_list()

#future_list

 

2. 全株のデータから2つの銘柄の組みあわせを抽出→2つの銘柄の組み合わせの距離を求める⇒算出した2銘柄の距離を tmp_distと表示する

 

2銘柄の距離を求めるには、割り算だったり、標準価格だったりを使用します。

 

def CalcDist(data,a='F_AE',b='F_AH'):

    df=data[[a,b]]

    norm_df=df/df.iloc[0]

   

    ret=norm_df.pct_change().dropna()

 

    std_price=np.cumprod(ret+1)

    tmp_dist=np.sum((std_price[a]-std_price[b]**2))

    return(tmp_dist)

 

 

3. 以下のコードは、距離の短い二銘柄を全株価のデータから見つけてきてます SuperPair=距離が短い2銘柄

 

 

前回算出した2銘柄の距離より、今回算出した2銘柄の距離が短いか長いかを確認→距離の短かった2銘柄を、次回以降距離を比較する際に使用する前回算出した距離データとして書き換える。

 

def SuperPair(data):

    assetnames=data.columns

    opt_pair=[]

    opt_dist=np.Inf

    for pair in itertools.combinations(assetnames,2):

        tmp_dist=CalcDist(data,pair[0],pair[1])

        

        if opt_dist>tmp_dist:

       

            opt_dist=tmp_dist

            opt_pair=pair[0],pair[1]

   

    

    tmp_dist=data[opt_pair[0]]-data[opt_pair[1]]

    sigma= tmp_dist.std()

 

    return(opt_pair,sigma)

 

3. AssetNameはデータ

 

AssetName=qndata.futures.load_data().asset

 

4. ぺあとれが儲けることができる投資手法なのかは、銘柄の価格を図示した際にぐにゃぐにゃになるかでわかるので、一応材料として以下で銘柄の価格を出しておきます。

 

5年間の株の価格データ

 

import qnt.data

import pandas as pd

data = qnt.data.futures.load_data(assets=AssetName.values,tail=365*5)

df = pd.DataFrame(data[0].values).dropna()

df.columns = AssetName.values

print(df)

 

5. さっきの5年間のデータを分割し、データの8割をtrain/2割をtestに充てます。

 

trainは似ている2銘柄を見つけてくるためのデータ testはその2銘柄を図示するとどのようにぐにゃぐにゃになるのかを検証するために使うデータ

 

from sklearn.model_selection import train_test_split

 

train,test=train_test_split(df,train_size=0.8,shuffle=False)

 

 

opt_pair=SuperPair(train)

 

6. 全データの内距離の短い2銘柄が見つかりました。('F_OJ', 'F_PA')のようです。

 

opt_pair[0]

 

7. 全データの内距離の短い2銘柄'F_OJ', 'F_PA')の株価を見ていきましょう。

 

pairvalues=test.loc[:,opt_pair[0]]

 

pairvalues

 

8. これまでで距離の短い2銘柄を求めてきた。

次はその2銘柄を何枚ずつ買うかのポートフォリオを探る。

 

ペアトレは2銘柄のうち、1銘柄を空売りしてその空売りで儲けたお金でもう1銘柄を購入するという手法なので、今回は'F_OJ'を空売り(-1)すると事前に決めて、'F_OJ'を空売り(-1)して儲けたお金の範囲で'F_PA'を何枚買うことができるのかを決めていく

 

 

メモ　コストは無しex.'F_EB'(1000円)を空売りして1000円儲けたらその1000円割る÷F_EDの値段で割ったらF_EDの買ったらよい枚数が定まる。

 

theta=(-1,pairvalues.iloc[0,0]/pairvalues.iloc[0,1])

theta

 

9. さっき決めたポートフォリオで2銘柄を購入すると2銘柄のポートフォリオ価値(合計金額)がどうなるかを出す

 

portValue=(theta[0]*pairvalues.iloc[:,0]+theta[1]*pairvalues.iloc[0,1])

portValue

 

10. 2銘柄のポートフォリオ価値(合計金額)を図示するとどうなるか見てみる

 

図示するとグラフがぐにゃぐにゃ=ペアトレは儲けることができる投資手法だと証明ができた。

 

import numpy as np

import matplotlib.pyplot as plt

 

plt.plot(portValue)

plt.show()

 

# 以上

 

 

 

 

