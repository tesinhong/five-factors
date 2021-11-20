import qnt.data as qndata
future_list = qndata.futures.load_list()
future_list
import plotly.graph_objs as go
futures_data = qndata.futures.load_data(tail = 365*15, dims = ("time", "field", "asset"))
data = futures_data.sel(asset= "F_AE").sel(field = 'close')
GBP_USD = futures_data.sel(asset = 'F_BP').sel(field = 'close')
trend_fig = [
    go.Scatter(
      x = GBP_USD.to_pandas().index,
      y = GBP_USD,
      name = "GBP_USD",
      line = dict(width=1, color='black')),
    go.Scatter(
      x = data.to_pandas().index,
      y = data,
      name = "data",
      line = dict(width=1, color="black"))
  ]

fig = go.Figure(data = trend_fig)
fig.update_yaxes(fixedrange=False)
#fig.add_trace(go.Scatter(x=GBP_USD.to_pandas().index, y=GBP_USD, name="GBP_USD", line = dict(width=1, color="black")))
#fig.add_trace(go.Scatter(x=data.to_pandas().index, y=data, name="data", line = dict(width=1, color="black")))
fig.update_xaxes(title="GBP_USD")
fig.update_yaxes(title="data")
fig.show()
#print(data)
#print(GBP_USD)
