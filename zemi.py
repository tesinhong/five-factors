import numpy as np
import pandas as pd
import qnt.data
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from numpy import array
a_data = qnt.data.futures.load_data(assets= ["F_AD"], min_date = "2021-06-01")
b_data = qnt.data.futures.load_data(assets= ["F_BO"], min_date = "2021-06-01")
sample_data = qnt.data.futures.load_data(assets= ["F_AD", "F_BO"], min_date = "2021-06-01")
close = sample_data.sel(field = "close")
a_close = a_data.sel(field="close")
b_close = b_data.sel(field = "close")
a = (a_close.to_pandas().tail())
b = (b_close.to_pandas().tail())
#print(a_close.values)
#print(a_close.to_pandas().values)
data = pd.DataFrame()
a_data = a_close.values
b_data = b_close.values
df = data({'F_AD': a})
#df.plot(title = 'F_AD and F_BO', grid = True)
#a_array = np.array(a_data)
#b_array = np.array(b_data)
#sample = [a_array, b_array]
#time = a_close.time
#print(time)
#print(data['F_AD': a_data, 'F_BO': b_data])
#for t in sample:
  #array = []
  #array = t
  #print(t)
  #data[t] = sample
#plt.plot(a_close.time,a_close, color = "black", linestyle = "solid", label = "NI225")
#plt.show()
#print(a_close.time)
