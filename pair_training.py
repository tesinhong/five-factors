# ペアートレーディング（ディスタンス法）

- 

import qnt.data as qndata
import numpy as np
import itertools

future_list=qndata.futures.load_list()
future_list

def CalcDist(data,a='F_AE',b='F_AH'):  

    df=data[[a,b]]
    norm_df=df/df.iloc[0]
    
    ret=norm_df.pct_change().dropna()
    
    std_price=np.cumprod(ret+1)
    tmp_dist=np.sum((std_price[a]-std_price[b]**2))
    return(tmp_dist)

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

AssetName=qndata.futures.load_data().asset

import qnt.data
import pandas as pd
data=qnt.data.futures.load_data(assets=AssetName[:].values,tail=365*10)
df=pd.DataFrame(data[0].values).dropna()
df.columns=AssetName[:].values
print(df)

from sklearn.model_selection import train_test_split

train,test=train_test_split(df,train_size=0.8,shuffle=False)

opt_pair=SuperPair(train)

opt_pair[0]

pairvalues=test.loc[:,opt_pair[0]]

pairvalues.iloc[0,0]

theta=(-1,pairvalues.iloc[0,0]/pairvalues.iloc[0,1])
theta

portValue=(theta[0]*pairvalues.iloc[:,0]+theta[1]*pairvalues.iloc[0,1])
portValue

import numpy as np
import matplotlib.pyplot as plt

plt.plot(portValue,color="b")
plt.show()

from sklearn.model_selection import train_test_split

train,test=train_test_split(df,test_size=40,shuffle=False)

opt_pair=SuperPair(train)

pairvalues=test.loc[:,opt_pair[0]]

theta=(-1,pairvalues.iloc[0,0]/pairvalues.iloc[0,1])
theta

portValue=(theta[0]*pairvalues.iloc[:,0]+theta[1]*pairvalues.iloc[0,1])
portValue

import numpy as np
import matplotlib.pyplot as plt

plt.plot(portVa
